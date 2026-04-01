#!/usr/bin/env python3
"""
VaultGuard API Server - AI-powered maintenance intelligence platform
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .llm_client import LLMClient
from .sheets_client import SheetsClient
from .invoice_processor import InvoiceProcessor


class InvoiceData(BaseModel):
    """Invoice data model"""
    invoice_id: str = Field(..., description="Invoice identifier")
    serial_number: str = Field(..., description="Safe serial number")
    safe_age_yr: Optional[float] = Field(None, description="Safe age in years")
    labour_charge: float = Field(..., description="Labour charge amount")
    parts_cost: float = Field(..., description="Parts cost amount")
    total_amount: float = Field(..., description="Total invoice amount")
    oos_tier1: str = Field("", description="Out of scope tier 1 category")
    oos_tier2: str = Field("", description="Out of scope tier 2 category")
    comment: str = Field("", description="Technician comment")
    current_decision: str = Field("UNKNOWN", description="Current billing decision")


class BillingDecision(BaseModel):
    """Billing decision result"""
    decision: str = Field(..., description="YES or NO for billing client")
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW confidence")
    reason: str = Field(..., description="Explanation for the decision")
    key_signal: str = Field(..., description="Key factor that drove the decision")
    flag_for_review: bool = Field(..., description="Whether to flag for manual review")


# Initialize MCP server
app = FastMCP("VaultGuard API", description="AI-powered smart safe maintenance billing validation")

# Initialize clients
llm_client = LLMClient()
sheets_client = SheetsClient()
invoice_processor = InvoiceProcessor(llm_client)


@app.tool()
async def classify_invoice(invoice_data: str) -> str:
    """
    Classify a maintenance invoice to determine if it should be billed to the client or absorbed by VaultGuard.

    Args:
        invoice_data: JSON string containing invoice information

    Returns:
        JSON string with classification decision
    """
    try:
        # Parse invoice data
        data = json.loads(invoice_data)
        invoice = InvoiceData(**data)

        # Classify using LLM
        decision = await invoice_processor.classify_invoice(invoice)

        return decision.model_dump_json()

    except Exception as e:
        return json.dumps({
            "error": f"Failed to classify invoice: {str(e)}",
            "decision": "UNKNOWN",
            "confidence": "LOW",
            "reason": "Classification failed due to error",
            "key_signal": "error",
            "flag_for_review": True
        })


@app.tool()
async def process_invoice_batch(invoice_batch: str, spreadsheet_id: str, sheet_name: str = "Invoices") -> str:
    """
    Process a batch of invoices and write results to Google Sheets.

    Args:
        invoice_batch: JSON string containing array of invoice objects
        spreadsheet_id: Google Sheets spreadsheet ID
        sheet_name: Name of the sheet to write to

    Returns:
        JSON string with processing results
    """
    try:
        # Parse batch data
        batch_data = json.loads(invoice_batch)
        invoices = [InvoiceData(**inv) for inv in batch_data]

        # Process each invoice
        results = []
        for invoice in invoices:
            decision = await invoice_processor.classify_invoice(invoice)
            results.append({
                "invoice": invoice.model_dump(),
                "decision": decision.model_dump()
            })

        # Write to Google Sheets
        await sheets_client.write_invoice_batch(spreadsheet_id, sheet_name, results)

        return json.dumps({
            "status": "success",
            "processed_count": len(results),
            "results": results
        })

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to process invoice batch: {str(e)}"
        })


@app.tool()
async def get_invoice_statistics(spreadsheet_id: str, sheet_name: str = "Invoices") -> str:
    """
    Get statistics from processed invoices in Google Sheets.

    Args:
        spreadsheet_id: Google Sheets spreadsheet ID
        sheet_name: Name of the sheet to read from

    Returns:
        JSON string with invoice statistics
    """
    try:
        stats = await sheets_client.get_invoice_statistics(spreadsheet_id, sheet_name)
        return json.dumps(stats)

    except Exception as e:
        return json.dumps({
            "error": f"Failed to get statistics: {str(e)}"
        })


@app.tool()
async def create_invoice_spreadsheet(title: str = "VaultGuard Invoices") -> str:
    """
    Create a new Google Sheets spreadsheet for invoice tracking.

    Args:
        title: Title for the new spreadsheet

    Returns:
        JSON string with spreadsheet information
    """
    try:
        spreadsheet = await sheets_client.create_spreadsheet(title)
        return json.dumps({
            "spreadsheet_id": spreadsheet.get('spreadsheetId'),
            "title": spreadsheet.get('properties', {}).get('title'),
            "url": f"https://docs.google.com/spreadsheets/d/{spreadsheet.get('spreadsheetId')}/edit"
        })

    except Exception as e:
        return json.dumps({
            "error": f"Failed to create spreadsheet: {str(e)}"
        })


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="VaultGuard API Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio",
                       help="Transport protocol to use")
    parser.add_argument("--port", type=int, default=8000,
                       help="Port for SSE transport")

    args = parser.parse_args()

    if args.transport == "sse":
        import uvicorn
        uvicorn.run(app.to_app(), host="0.0.0.0", port=args.port)
    else:
        # Run with stdio transport
        import sys
        import asyncio

        async def run_stdio():
            async with app.to_app().lifespan():
                await app.run_stdio_async()

        asyncio.run(run_stdio())


if __name__ == "__main__":
    main()