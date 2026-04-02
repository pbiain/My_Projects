#!/usr/bin/env python3
"""
LLM Client for VaultGuard API Server
"""

import os
from typing import Optional

from openai import AsyncOpenAI
from langsmith import Client as LangSmithClient, traceable
from langsmith.wrappers import wrap_openai
import json


class LLMClient:
    """Client for interacting with OpenAI and LangSmith"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            # wrap_openai automatically traces all calls to LangSmith
            self.openai_client = wrap_openai(AsyncOpenAI(api_key=api_key))
        else:
            self.openai_client = None

        # Initialize LangSmith if API key is provided
        langsmith_key = os.getenv("LANGCHAIN_API_KEY")
        if langsmith_key and langsmith_key != "your_langchain_api_key_here":
            self.langsmith_client = LangSmithClient(api_key=langsmith_key)
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "vaultguard-billing")
        else:
            self.langsmith_client = None

    def _redact_pii(self, invoice_data: dict) -> dict:
        """
        Remove customer PII before sending invoice data to any external LLM.
        GDPR: customer name, address, and contact details are not required
        for billing classification and must not leave the system boundary.
        """
        import hashlib
        redacted = invoice_data.copy()
        # Replace identifying fields with a consistent pseudonym
        # (same customer always gets same token — useful for audit)
        raw_id = (
            str(redacted.get("ship_name", ""))
            + str(redacted.get("ship_addr1", ""))
            + str(redacted.get("ship_zip", ""))
        )
        token = "CLIENT-" + hashlib.sha256(raw_id.encode()).hexdigest()[:8].upper()

        for field in ("ship_name", "ship_addr1", "ship_city", "ship_state", "ship_zip"):
            if field in redacted:
                redacted[field] = token
        return redacted

    @traceable(name="classify_invoice", run_type="llm")
    async def classify_invoice(self, invoice_data: dict) -> dict:
        """
        Classify an invoice using GPT-4o

        Args:
            invoice_data: Dictionary containing invoice information

        Returns:
            Dictionary with classification decision
        """
        # Return mock response if OpenAI client not available
        if not self.openai_client:
            return self._mock_classification(invoice_data)

        # Redact PII before sending to external LLM (GDPR)
        invoice_data = self._redact_pii(invoice_data)

        system_prompt = """You are a billing validation AI for VaultGuard Inc., a cash management company. You analyse smart safe maintenance invoices to determine whether the cost should be billed to the client (YES) or absorbed by VaultGuard (NO).

DECISION RULES (from White Glove Service Contract):

BILL CLIENT (YES) when the issue is caused by:
- Abuse, misuse, vandalism, or negligence
- Liquid spillage onto equipment
- Physical damage (broken/cracked screen, bent components)
- Foreign objects in bill acceptors (coins, debris)
- Infestation (insects, rodents)
- Safe burglary or robbery attempt damage
- Customer refused access or cancelled after dispatch

ABSORB (NO) when the issue is:
- Normal wear and tear (validator spring/component failure)
- Communications / connectivity / modem failure
- Software or firmware issues
- Network or phone line problems
- User programming errors
- No problem found on site
- Printer jams or paper loading
- Equipment resets

IMPORTANT: The labour charge tells you the call type:
- $186 or $189 = standard OOS rate (Zone 1-3)
- $621 or $630 = remote OOS rate (Zone 4)
Both indicate the visit was classified as Out of Scope by the technician.

Respond ONLY with valid JSON in this exact format, no preamble, no markdown:
{
  "decision": "YES" or "NO",
  "confidence": "HIGH", "MEDIUM", or "LOW",
  "reason": "one sentence explaining the decision",
  "key_signal": "the specific word or phrase that drove the decision",
  "flag_for_review": true or false
}

Set flag_for_review to true when:
- Confidence is LOW
- The comment is empty or ambiguous
- The OOS tier categories are missing
- There is a conflict between the comment and the OOS categories"""

        user_prompt = f"""=== INVOICE TO CLASSIFY ===

Invoice ID:      {invoice_data.get('invoice_id', 'UNKNOWN')}
Serial Number:   {invoice_data.get('serial_number', 'UNKNOWN')}
Safe Age:        {f"{invoice_data.get('safe_age_yr')} years" if invoice_data.get('safe_age_yr') else 'Unknown'}
Labour Charge:   ${invoice_data.get('labour_charge', 0)}
Parts Cost:      ${invoice_data.get('parts_cost', 0)}
Total Amount:    ${invoice_data.get('total_amount', 0)}
OOS Tier 1:      {invoice_data.get('oos_tier1', 'Not provided')}
OOS Tier 2:      {invoice_data.get('oos_tier2', 'Not provided')}
Technician Note: {invoice_data.get('comment', 'No comment provided')}
Current Decision: {invoice_data.get('current_decision', 'UNKNOWN')}

Classify this invoice."""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            # Validate response format
            required_fields = ["decision", "confidence", "reason", "key_signal", "flag_for_review"]
            if not all(field in result for field in required_fields):
                raise ValueError("Invalid response format from LLM")

            return result

        except Exception as e:
            # Return error response
            return {
                "decision": "UNKNOWN",
                "confidence": "LOW",
                "reason": f"Classification failed: {str(e)}",
                "key_signal": "error",
                "flag_for_review": True
            }

    def _mock_classification(self, invoice_data: dict) -> dict:
        """
        Return mock classification for testing when OpenAI is not available

        Args:
            invoice_data: Invoice data

        Returns:
            Mock classification result
        """
        # Simple rule-based mock classification
        comment = invoice_data.get('comment', '').lower()
        oos_tier1 = invoice_data.get('oos_tier1', '').lower()

        # Check for billable indicators
        billable_keywords = ['damage', 'broken', 'cracked', 'smashed', 'abuse', 'vandalism', 'liquid', 'spillage']
        absorb_keywords = ['wear', 'tear', 'software', 'firmware', 'communication', 'network', 'programming']

        billable_score = sum(1 for keyword in billable_keywords if keyword in comment or keyword in oos_tier1)
        absorb_score = sum(1 for keyword in absorb_keywords if keyword in comment or keyword in oos_tier1)

        if billable_score > absorb_score:
            decision = "YES"
            reason = "Detected indicators of customer-caused damage"
            confidence = "HIGH"
        elif absorb_score > billable_score:
            decision = "NO"
            reason = "Issue appears to be normal wear or technical failure"
            confidence = "HIGH"
        else:
            decision = "NO"
            reason = "Unable to determine cause from available information"
            confidence = "LOW"

        return {
            "decision": decision,
            "confidence": confidence,
            "reason": reason,
            "key_signal": invoice_data.get('comment', 'insufficient data'),
            "flag_for_review": confidence == "LOW" or not invoice_data.get('comment')
        }

    async def extract_invoice_data(self, pdf_base64: str, filename: str) -> list[dict]:
        """
        Extract invoice data from an image-based PDF using GPT-4o vision.
        Uses pymupdf to render each page as a PNG, then sends images to GPT-4o.

        GDPR NOTE: Page images (including customer PII) are sent to OpenAI here —
        this is the only step where PII leaves the system. All subsequent
        LLM calls (classification) use _redact_pii() first.

        Args:
            pdf_base64: Standard base64-encoded PDF content
            filename: Original filename

        Returns:
            List of invoice dictionaries extracted from the PDF
        """
        import base64
        import io
        import fitz  # pymupdf

        if not self.openai_client:
            raise ValueError("OpenAI client not configured")

        # Render each PDF page as a PNG image
        pdf_bytes = base64.b64decode(pdf_base64)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        image_contents = []
        for page in doc:
            # Redact all embedded images (logos, stamps) before rendering — GDPR/confidentiality
            for img in page.get_images(full=True):
                xref = img[0]
                rects = page.get_image_rects(xref)
                for rect in rects:
                    page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

            # Render at 150 DPI — enough for OCR, small enough for API
            mat = fitz.Matrix(150 / 72, 150 / 72)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            img_b64 = base64.b64encode(img_bytes).decode()
            image_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_b64}",
                    "detail": "high"
                }
            })

        doc.close()

        # Add extraction prompt after images
        image_contents.append({
            "type": "text",
            "text": (
                "Extract all invoice line items from these SafeCore service invoice pages. "
                "Return a JSON array where each element represents one invoice with these exact fields: "
                "invoice_number, invoice_date, serial_number, branch_number, po_number, "
                "ship_name, ship_addr1, ship_city, ship_state, ship_zip, call_number, "
                "labor_charge (number), parts_amount (number), shipping_amount (number), "
                "subtotal (number), tax_amount (number), total_amount (number), "
                "oos_tier1, oos_tier2, comment. "
                "Return ONLY the JSON array, no markdown, no preamble."
            )
        })

        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": image_contents}],
            temperature=0.1,
            max_tokens=16000
        )

        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason

        # Strip markdown fences
        clean = content.replace("```json", "").replace("```", "").strip()

        # If response was cut off, try to salvage partial JSON by closing the array
        if finish_reason == "length" and not clean.endswith("]"):
            # Close last incomplete object and the array
            last_brace = clean.rfind("}")
            if last_brace != -1:
                clean = clean[:last_brace + 1] + "]"
            else:
                clean = clean + "}]"

        try:
            invoices = json.loads(clean)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"GPT-4o returned invalid JSON (finish_reason={finish_reason}). "
                f"Parse error: {e}. "
                f"Response preview: {content[:500]}"
            )

        if not isinstance(invoices, list):
            invoices = [invoices]
        return invoices