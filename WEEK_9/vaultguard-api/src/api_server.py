#!/usr/bin/env python3
"""
REST API Server for VaultGuard — n8n integration endpoint
"""

import os
import asyncio
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

from .llm_client import LLMClient
from .invoice_processor import InvoiceProcessor, InvoiceData

app = FastAPI(title="VaultGuard API", description="REST wrapper for n8n integration")

llm_client = LLMClient()
invoice_processor = InvoiceProcessor(llm_client)

GL_CODE_YES = 440134
GL_CODE_NO = 440133


class ExtractRequest(BaseModel):
    """PDF extraction request — accepts base64 PDF from Gmail"""
    data: str  # URL-safe or standard base64
    pdfName: str = "invoice.pdf"
    batchName: str = ""
    processedAt: str = ""


class ClassifyRequest(BaseModel):
    """Accepts both standard API field names and n8n workflow field names"""
    # Standard API fields
    invoice_id: Optional[str] = None
    serial_number: Optional[str] = None
    safe_age_yr: Optional[float] = None
    labour_charge: Optional[float] = None
    parts_cost: Optional[float] = None
    total_amount: Optional[float] = None
    oos_tier1: Optional[str] = ""
    oos_tier2: Optional[str] = ""
    comment: Optional[str] = ""
    current_decision: Optional[str] = "UNKNOWN"
    # n8n workflow field aliases
    invoice_number: Optional[str] = None
    labor_charge: Optional[float] = None
    parts_amount: Optional[float] = None


@app.post("/extract")
async def extract_invoices(req: ExtractRequest):
    """Extract invoices from a base64 PDF — called once per email by n8n"""
    # Gmail returns URL-safe base64 — normalize to standard
    standard_b64 = req.data.replace("-", "+").replace("_", "/")
    try:
        invoices = await llm_client.extract_invoice_data(standard_b64, req.pdfName)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    return {
        "invoices": invoices,
        "batchName": req.batchName,
        "processedAt": req.processedAt,
        "count": len(invoices)
    }


@app.post("/classify")
async def classify_invoice(req: ClassifyRequest):
    """Classify a single invoice — called by n8n for each invoice in the batch"""
    invoice = InvoiceData(
        invoice_id=req.invoice_id or req.invoice_number or "UNKNOWN",
        serial_number=req.serial_number or "UNKNOWN",
        safe_age_yr=req.safe_age_yr,
        labour_charge=req.labour_charge or req.labor_charge or 0,
        parts_cost=req.parts_cost or req.parts_amount or 0,
        total_amount=req.total_amount or 0,
        oos_tier1=req.oos_tier1 or "",
        oos_tier2=req.oos_tier2 or "",
        comment=req.comment or "",
        current_decision=req.current_decision or "UNKNOWN",
    )

    try:
        decision = await invoice_processor.classify_invoice(invoice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

    result = {
        "decision": decision.decision,
        "gl_code": GL_CODE_YES if decision.decision == "YES" else GL_CODE_NO,
        "confidence": decision.confidence,
        "reason": decision.reason,
        "key_signal": decision.key_signal,
        "flag_for_review": decision.flag_for_review,
    }

    # Auto-log to LangSmith when we have a known human decision to compare against
    human_decision = (req.current_decision or "UNKNOWN").strip().upper()
    if human_decision in ("YES", "NO") and llm_client.langsmith_client:
        try:
            _log_to_langsmith(invoice, result, human_decision)
        except Exception as e:
            print(f"LangSmith logging error: {e}")
    else:
        print(f"Skipping LangSmith log — human_decision={human_decision!r}, langsmith_client={llm_client.langsmith_client is not None}")

    return result


def _log_to_langsmith(invoice: InvoiceData, ai_result: dict, human_decision: str):
    """Log a real invoice classification to LangSmith as a labelled example."""
    dataset_name = "VaultGuard — Real Invoice Evaluations"
    ls = llm_client.langsmith_client

    if not ls.has_dataset(dataset_name=dataset_name):
        ls.create_dataset(
            dataset_name=dataset_name,
            description="Live invoice classifications — AI vs human biller"
        )

    dataset = ls.read_dataset(dataset_name=dataset_name)

    ls.create_examples(
        inputs=[{
            "invoice_id":    invoice.invoice_id,
            "serial_number": invoice.serial_number,
            "labour_charge": invoice.labour_charge,
            "parts_cost":    invoice.parts_cost,
            "total_amount":  invoice.total_amount,
            "oos_tier1":     invoice.oos_tier1,
            "oos_tier2":     invoice.oos_tier2,
            "comment":       invoice.comment,
        }],
        outputs=[{
            "expected_decision": human_decision,
            "ai_decision":       ai_result["decision"],
            "ai_confidence":     ai_result["confidence"],
            "ai_reason":         ai_result["reason"],
            "match":             human_decision == ai_result["decision"],
        }],
        dataset_id=dataset.id
    )
    print(f"Logged to LangSmith: {invoice.invoice_id} | human={human_decision} | ai={ai_result['decision']}")


@app.get("/health")
async def health():
    return {"status": "ok", "openai_configured": llm_client.openai_client is not None}


def main():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
