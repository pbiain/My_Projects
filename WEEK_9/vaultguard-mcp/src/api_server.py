#!/usr/bin/env python3
"""
REST API Server for VaultGuard — n8n integration endpoint
"""

import os
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


class ClassifyRequest(BaseModel):
    """Accepts both MCP field names and n8n workflow field names"""
    # Standard MCP fields
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

    return {
        "decision": decision.decision,
        "gl_code": GL_CODE_YES if decision.decision == "YES" else GL_CODE_NO,
        "confidence": decision.confidence,
        "reason": decision.reason,
        "key_signal": decision.key_signal,
        "flag_for_review": decision.flag_for_review,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "openai_configured": llm_client.openai_client is not None}


def main():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
