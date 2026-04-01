#!/usr/bin/env python3
"""
LLM Client for VaultGuard MCP Server
"""

import os
from typing import Optional

from openai import AsyncOpenAI
from langsmith import Client as LangSmithClient
import json


class LLMClient:
    """Client for interacting with OpenAI and LangSmith"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            self.openai_client = AsyncOpenAI(api_key=api_key)
        else:
            self.openai_client = None

        # Initialize LangSmith if API key is provided
        langsmith_key = os.getenv("LANGCHAIN_API_KEY")
        if langsmith_key and langsmith_key != "your_langchain_api_key_here":
            self.langsmith_client = LangSmithClient(api_key=langsmith_key)
        else:
            self.langsmith_client = None

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

    async def extract_invoice_data(self, pdf_content: bytes, filename: str) -> dict:
        """
        Extract invoice data from PDF content using GPT-4o vision

        Args:
            pdf_content: PDF file content as bytes
            filename: Original filename

        Returns:
            Dictionary with extracted invoice data
        """
        # For now, return a placeholder - in production this would use PDF parsing
        # and potentially GPT-4 vision for OCR
        return {
            "invoice_id": f"PDF-{filename}",
            "serial_number": "EXTRACTED_FROM_PDF",
            "safe_age_yr": None,
            "labour_charge": 186.0,
            "parts_cost": 0.0,
            "total_amount": 186.0,
            "oos_tier1": "",
            "oos_tier2": "",
            "comment": "Extracted from PDF",
            "current_decision": "UNKNOWN"
        }