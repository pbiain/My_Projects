#!/usr/bin/env python3
"""
LangSmith evaluation for VaultGuard billing classifier.

Runs a labelled dataset of invoices through the classifier and measures
decision accuracy against known correct answers.

Usage:
    python evals/evaluate_classifier.py
"""

import asyncio
import os
from dotenv import load_dotenv
from langsmith import Client, evaluate
from langsmith.schemas import Run, Example

load_dotenv()

# ── Labelled test dataset ──────────────────────────────────────────────────
# Each example has an invoice and the correct billing decision.
# These are based on the 2025 historical dataset where the human biller
# and the AI agreed with HIGH confidence.

EXAMPLES = [
    {
        "invoice_id": "EVAL-001",
        "serial_number": "CT-00441",
        "labour_charge": 189,
        "parts_cost": 0,
        "total_amount": 196.25,
        "oos_tier1": "Non-Device Related Issue",
        "oos_tier2": "Comms",
        "comment": "On arrival accessed safe, replaced antenna. Called and confirmed comms. Safe up and running.",
        "current_decision": "NO",
        "expected_decision": "NO",
        "reason": "Antenna/comms replacement is normal wear — covered under contract"
    },
    {
        "invoice_id": "EVAL-002",
        "serial_number": "FB-03109",
        "labour_charge": 189,
        "parts_cost": 45.0,
        "total_amount": 241.50,
        "oos_tier1": "Device Related Issue",
        "oos_tier2": "Physical Damage",
        "comment": "Safe screen cracked. Customer advised drinks were spilled on unit. Replaced display.",
        "current_decision": "YES",
        "expected_decision": "YES",
        "reason": "Liquid spillage causing physical damage — client responsibility"
    },
    {
        "invoice_id": "EVAL-003",
        "serial_number": "CU-01602",
        "labour_charge": 189,
        "parts_cost": 0,
        "total_amount": 200.34,
        "oos_tier1": "Non-Device Related Issue",
        "oos_tier2": "No Fault Found",
        "comment": "Met manager on arrival, stated safe is working fine. Observed a successful drop.",
        "current_decision": "NO",
        "expected_decision": "NO",
        "reason": "No fault found — absorb cost of unnecessary visit"
    },
    {
        "invoice_id": "EVAL-004",
        "serial_number": "BT-00872",
        "labour_charge": 189,
        "parts_cost": 0,
        "total_amount": 196.25,
        "oos_tier1": "Device Related Issue",
        "oos_tier2": "Foreign Object",
        "comment": "Found coins and debris jammed in bill acceptor slot. Cleared obstruction, tested ok.",
        "current_decision": "YES",
        "expected_decision": "YES",
        "reason": "Foreign object — client negligence, not covered by contract"
    },
    {
        "invoice_id": "EVAL-005",
        "serial_number": "GH-00312",
        "labour_charge": 189,
        "parts_cost": 12.50,
        "total_amount": 208.85,
        "oos_tier1": "Non-Device Related Issue",
        "oos_tier2": "Software",
        "comment": "Safe displaying error code E4. Performed firmware update remotely, safe operational.",
        "current_decision": "NO",
        "expected_decision": "NO",
        "reason": "Firmware issue — software/technical failure covered under contract"
    },
    {
        "invoice_id": "EVAL-006",
        "serial_number": "MK-00541",
        "labour_charge": 189,
        "parts_cost": 0,
        "total_amount": 196.25,
        "oos_tier1": "Device Related Issue",
        "oos_tier2": "Physical Damage",
        "comment": "Pry marks visible on safe door. Customer reports break-in attempt over the weekend.",
        "current_decision": "YES",
        "expected_decision": "YES",
        "reason": "Burglary damage — client premises security issue, not contract coverage"
    },
    {
        "invoice_id": "EVAL-007",
        "serial_number": "RT-00229",
        "labour_charge": 189,
        "parts_cost": 28.0,
        "total_amount": 224.34,
        "oos_tier1": "Non-Device Related Issue",
        "oos_tier2": "Validator",
        "comment": "Validator spring worn, replaced. Safe counting correctly after repair.",
        "current_decision": "NO",
        "expected_decision": "NO",
        "reason": "Validator wear — normal component end of life, covered under contract"
    },
    {
        "invoice_id": "EVAL-008",
        "serial_number": "PQ-00118",
        "labour_charge": 189,
        "parts_cost": 0,
        "total_amount": 196.25,
        "oos_tier1": "Non-Device Related Issue",
        "oos_tier2": "Customer Training",
        "comment": "Customer had set wrong denomination in settings. Corrected configuration, demonstrated correct use.",
        "current_decision": "NO",
        "expected_decision": "NO",
        "reason": "User programming error — covered, not client negligence"
    },
]


# ── Evaluator ─────────────────────────────────────────────────────────────

def decision_correct(run: Run, example: Example) -> dict:
    """Check if the AI decision matches the expected decision."""
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
    """Check that HIGH confidence decisions are actually correct."""
    ai_output = run.outputs or {}
    expected = example.outputs.get("expected_decision", "")
    actual = ai_output.get("decision", "UNKNOWN")
    confidence = ai_output.get("confidence", "LOW")

    # Penalise HIGH confidence wrong answers — these are the dangerous ones
    if confidence == "HIGH" and actual != expected:
        return {"key": "confidence_appropriate", "score": 0,
                "comment": "HIGH confidence but wrong — dangerous"}
    return {"key": "confidence_appropriate", "score": 1,
            "comment": f"Confidence {confidence} is appropriate"}


# ── Target function ────────────────────────────────────────────────────────

def classify_invoice_sync(inputs: dict) -> dict:
    """Synchronous wrapper for the async classifier — needed by LangSmith evaluate()."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.llm_client import LLMClient

    client = LLMClient()
    result = asyncio.run(client.classify_invoice(inputs))
    return result


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    ls_client = Client()
    dataset_name = "VaultGuard Billing Classifier — Labelled"

    # Create or update dataset in LangSmith
    if not ls_client.has_dataset(dataset_name=dataset_name):
        dataset = ls_client.create_dataset(
            dataset_name=dataset_name,
            description="Labelled invoice examples for billing classification evaluation"
        )
        ls_client.create_examples(
            inputs=[{k: v for k, v in ex.items()
                     if k not in ("expected_decision", "reason")} for ex in EXAMPLES],
            outputs=[{"expected_decision": ex["expected_decision"],
                      "reason": ex["reason"]} for ex in EXAMPLES],
            dataset_id=dataset.id
        )
        print(f"Created dataset with {len(EXAMPLES)} examples")
    else:
        print(f"Using existing dataset: {dataset_name}")

    # Run evaluation
    results = evaluate(
        classify_invoice_sync,
        data=dataset_name,
        evaluators=[decision_correct, confidence_appropriate],
        experiment_prefix="vaultguard-billing",
        metadata={"model": "gpt-4o", "temperature": 0.1}
    )

    # Print summary
    print("\n=== EVALUATION RESULTS ===")
    correct = sum(1 for r in results for m in r.get("evaluation_results", {}).get("results", [])
                  if m.key == "decision_correct" and m.score == 1)
    total = len(EXAMPLES)
    print(f"Decision accuracy: {correct}/{total} ({100*correct/total:.1f}%)")
    print(f"\nFull results in LangSmith: https://smith.langchain.com")


if __name__ == "__main__":
    main()
