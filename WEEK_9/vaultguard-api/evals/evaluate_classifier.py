#!/usr/bin/env python3
"""
LangSmith evaluation for VaultGuard billing classifier.

Uses real invoice classifications logged automatically by the API server.
Run the n8n pipeline first to populate the dataset, then run this script.

Usage:
    python evals/evaluate_classifier.py
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from langsmith import Client, evaluate
from langsmith.schemas import Run, Example

load_dotenv()

REAL_DATASET = "VaultGuard — Real Invoice Evaluations"


# ── Evaluators ────────────────────────────────────────────────────────────

def decision_correct(run: Run, example: Example) -> dict:
    """Check if the AI decision matches the human biller's decision."""
    ai_output = run.outputs or {}
    expected = example.outputs.get("expected_decision", "")
    actual = ai_output.get("decision", "UNKNOWN")

    correct = actual == expected
    return {
        "key": "decision_correct",
        "score": 1 if correct else 0,
        "comment": f"Expected {expected}, got {actual}"
    }


def confidence_appropriate(run: Run, example: Example) -> dict:
    """Penalise HIGH confidence wrong answers — these are the dangerous ones."""
    ai_output = run.outputs or {}
    expected = example.outputs.get("expected_decision", "")
    actual = ai_output.get("decision", "UNKNOWN")
    confidence = ai_output.get("confidence", "LOW")

    if confidence == "HIGH" and actual != expected:
        return {"key": "confidence_appropriate", "score": 0,
                "comment": "HIGH confidence but wrong — dangerous"}
    return {"key": "confidence_appropriate", "score": 1,
            "comment": f"Confidence {confidence} is appropriate"}


# ── Target function ────────────────────────────────────────────────────────

def classify_invoice_sync(inputs: dict) -> dict:
    """Synchronous wrapper for the async classifier."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.llm_client import LLMClient

    client = LLMClient()
    return asyncio.run(client.classify_invoice(inputs))


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    ls_client = Client()

    if not ls_client.has_dataset(dataset_name=REAL_DATASET):
        print("No real invoice data yet. Run the n8n pipeline first to populate the dataset.")
        return

    examples = list(ls_client.list_examples(dataset_name=REAL_DATASET))
    if not examples:
        print("Dataset exists but has no examples yet. Run the n8n pipeline first.")
        return

    print(f"Evaluating {len(examples)} real invoices from LangSmith dataset...")

    results = evaluate(
        classify_invoice_sync,
        data=REAL_DATASET,
        evaluators=[decision_correct, confidence_appropriate],
        experiment_prefix="vaultguard-billing",
        metadata={"model": "gpt-4o", "temperature": 0.1}
    )

    total = len(list(results))
    print(f"\n=== EVALUATION RESULTS ===")
    print(f"Evaluated: {total} real invoices")
    print(f"Full results: smith.langchain.com")


if __name__ == "__main__":
    main()
