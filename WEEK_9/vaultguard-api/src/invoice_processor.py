#!/usr/bin/env python3
"""
Invoice Processor for VaultGuard API Server
"""

from typing import Dict, Any
from pydantic import BaseModel

from .llm_client import LLMClient


class InvoiceData(BaseModel):
    """Invoice data model"""
    invoice_id: str
    serial_number: str
    safe_age_yr: float = None
    labour_charge: float
    parts_cost: float
    total_amount: float
    oos_tier1: str = ""
    oos_tier2: str = ""
    comment: str = ""
    current_decision: str = "UNKNOWN"


class BillingDecision(BaseModel):
    """Billing decision result"""
    decision: str  # "YES" or "NO"
    confidence: str  # "HIGH", "MEDIUM", or "LOW"
    reason: str
    key_signal: str
    flag_for_review: bool


class InvoiceProcessor:
    """Processes invoices using LLM classification"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def classify_invoice(self, invoice: InvoiceData) -> BillingDecision:
        """
        Classify a single invoice

        Args:
            invoice: InvoiceData object

        Returns:
            BillingDecision object
        """
        # Convert to dict for LLM processing
        invoice_dict = invoice.model_dump()

        # Get classification from LLM
        result = await self.llm_client.classify_invoice(invoice_dict)

        # Create and return BillingDecision
        return BillingDecision(**result)

    async def process_invoice_batch(self, invoices: list[InvoiceData]) -> list[Dict[str, Any]]:
        """
        Process a batch of invoices

        Args:
            invoices: List of InvoiceData objects

        Returns:
            List of processing results
        """
        results = []
        for invoice in invoices:
            decision = await self.classify_invoice(invoice)
            results.append({
                "invoice": invoice.model_dump(),
                "decision": decision.model_dump()
            })

        return results

    def normalize_invoice_data(self, raw_data: Dict[str, Any]) -> InvoiceData:
        """
        Normalize raw invoice data to standard format

        Args:
            raw_data: Raw invoice data dictionary

        Returns:
            Normalized InvoiceData object
        """
        # Handle various field name mappings
        normalized = {
            "invoice_id": raw_data.get("invoice_id") or raw_data.get("PO") or f"INV-{len(raw_data)}",
            "serial_number": raw_data.get("serial_number") or raw_data.get("Serial Number") or "UNKNOWN",
            "safe_age_yr": raw_data.get("safe_age_yr") or raw_data.get("Safe manufacture year"),
            "labour_charge": float(raw_data.get("labour_charge") or raw_data.get("Lineitem_1_UnitPrice") or 0),
            "parts_cost": float(raw_data.get("parts_cost") or raw_data.get("Lineitem_2_UnitPrice") or 0),
            "total_amount": float(raw_data.get("total_amount") or raw_data.get("Total Invoice Amount") or 0),
            "oos_tier1": raw_data.get("oos_tier1") or raw_data.get("OOS Tier 1 Category") or "",
            "oos_tier2": raw_data.get("oos_tier2") or raw_data.get("OOS Tier 2 Category") or "",
            "comment": raw_data.get("comment") or raw_data.get("InvoiceComment") or "",
            "current_decision": raw_data.get("current_decision") or raw_data.get("Bill Customer") or "UNKNOWN"
        }

        return InvoiceData(**normalized)