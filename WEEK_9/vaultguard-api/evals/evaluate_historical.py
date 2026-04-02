#!/usr/bin/env python3
"""
Historical accuracy evaluation for VaultGuard billing classifier.

Loads the 2025 maintenance dataset (with human biller decisions) into
LangSmith and runs the AI classifier against it to measure accuracy.

Usage:
    python evals/evaluate_historical.py              # 50 invoices (default)
    python evals/evaluate_historical.py --sample 100 # custom sample size
    python evals/evaluate_historical.py --all        # full dataset (expensive)
"""

import asyncio
import sys
import os
import argparse
import pandas as pd
from dotenv import load_dotenv
from langsmith import Client, evaluate
from langsmith.schemas import Run, Example

load_dotenv()

DATASET_NAME = "VaultGuard — Historical 2025 Invoices"
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "Documents", "Copy of 251120-251114TIDELSER-MR01WORKING.xlsx")


# ── Load and prepare data ─────────────────────────────────────────────────

def load_invoices(sample: int = 50, use_all: bool = False) -> list[dict]:
    df = pd.read_excel(EXCEL_PATH)

    # Keep only rows with a clear YES/NO decision
    df = df[df["Bill Customer"].isin(["YES", "NO"])].copy()

    # Map columns to API field names
    df["invoice_id"]    = df["Invoice"].astype(str)
    df["serial_number"] = df["Serial Number"].astype(str)
    df["safe_age_yr"]   = None
    df["labour_charge"] = pd.to_numeric(df["Labor Charge"], errors="coerce").fillna(0)
    df["parts_cost"]    = pd.to_numeric(df.get("Sub Total", 0), errors="coerce").fillna(0)
    df["total_amount"]  = pd.to_numeric(df["Total Invoice Amount"], errors="coerce").fillna(0)
    df["comment"]       = df["InvoiceComment"].fillna("").astype(str)
    df["oos_tier1"]     = df["OOS Tier Categories"].fillna("").astype(str)
    df["oos_tier2"]     = df["OOS 2 Tier Categories"].fillna("").astype(str)
    df["expected"]      = df["Bill Customer"]

    if not use_all:
        # Balanced sample — equal YES and NO
        half = sample // 2
        yes_rows = df[df["expected"] == "YES"].sample(min(half, len(df[df["expected"] == "YES"])), random_state=42)
        no_rows  = df[df["expected"] == "NO"].sample(min(half, len(df[df["expected"] == "NO"])),  random_state=42)
        df = pd.concat([yes_rows, no_rows])

    fields = ["invoice_id", "serial_number", "safe_age_yr", "labour_charge",
              "parts_cost", "total_amount", "comment", "oos_tier1", "oos_tier2", "expected"]
    return df[fields].to_dict(orient="records")


# ── Evaluators ────────────────────────────────────────────────────────────

def decision_correct(run: Run, example: Example) -> dict:
    ai_output = run.outputs or {}
    expected = example.outputs.get("expected_decision", "")
    actual   = ai_output.get("decision", "UNKNOWN")
    return {
        "key": "decision_correct",
        "score": 1 if actual == expected else 0,
        "comment": f"Expected {expected}, got {actual}"
    }


def judge_agrees(run: Run, example: Example) -> dict:
    ai_output = run.outputs or {}
    verdict = ai_output.get("judge_verdict", "UNCERTAIN")
    score = 1 if verdict == "AGREE" else (0 if verdict == "DISAGREE" else 0.5)
    return {
        "key": "judge_agrees",
        "score": score,
        "comment": f"Judge verdict: {verdict} — {ai_output.get('judge_reason', '')}"
    }


def confidence_appropriate(run: Run, example: Example) -> dict:
    ai_output  = run.outputs or {}
    expected   = example.outputs.get("expected_decision", "")
    actual     = ai_output.get("decision", "UNKNOWN")
    confidence = ai_output.get("confidence", "LOW")
    if confidence == "HIGH" and actual != expected:
        return {"key": "confidence_appropriate", "score": 0,
                "comment": "HIGH confidence but wrong — dangerous"}
    return {"key": "confidence_appropriate", "score": 1,
            "comment": f"Confidence {confidence} is appropriate"}


# ── Target function ────────────────────────────────────────────────────────

def classify_invoice_sync(inputs: dict) -> dict:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.llm_client import LLMClient

    async def run():
        client = LLMClient()
        result = await client.classify_invoice(inputs)
        judge = await client.judge_classification(inputs, result)
        result["judge_verdict"] = judge.get("verdict", "UNCERTAIN")
        result["judge_reason"] = judge.get("reason", "")
        if judge.get("verdict") == "DISAGREE":
            result["flag_for_review"] = True
        return result

    return asyncio.run(run())


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=50, help="Number of invoices to sample")
    parser.add_argument("--all", action="store_true", help="Run on full dataset (expensive)")
    args = parser.parse_args()

    invoices = load_invoices(sample=args.sample, use_all=args.all)
    print(f"Loaded {len(invoices)} invoices ({sum(1 for i in invoices if i['expected'] == 'YES')} YES, "
          f"{sum(1 for i in invoices if i['expected'] == 'NO')} NO)")

    ls_client = Client()

    # Recreate dataset fresh each run so results stay current
    if ls_client.has_dataset(dataset_name=DATASET_NAME):
        ls_client.delete_dataset(dataset_name=DATASET_NAME)

    dataset = ls_client.create_dataset(
        dataset_name=DATASET_NAME,
        description=f"2025 historical invoices — human biller ground truth ({len(invoices)} sample)"
    )
    ls_client.create_examples(
        inputs=[{k: v for k, v in inv.items() if k != "expected"} for inv in invoices],
        outputs=[{"expected_decision": inv["expected"]} for inv in invoices],
        dataset_id=dataset.id
    )
    print(f"Dataset ready in LangSmith. Running classifier...")

    results = list(evaluate(
        classify_invoice_sync,
        data=DATASET_NAME,
        evaluators=[decision_correct, confidence_appropriate, judge_agrees],
        experiment_prefix="vaultguard-historical",
        metadata={"model": "gpt-4o", "temperature": 0.1, "sample": len(invoices)}
    ))

    # Summary
    correct = sum(
        1 for r in results
        for m in (r.get("evaluation_results") or {}).get("results", [])
        if getattr(m, "key", None) == "decision_correct" and getattr(m, "score", 0) == 1
    )
    dangerous = sum(
        1 for r in results
        for m in (r.get("evaluation_results") or {}).get("results", [])
        if getattr(m, "key", None) == "confidence_appropriate" and getattr(m, "score", 0) == 0
    )

    print(f"\n=== RESULTS ===")
    print(f"Accuracy:          {correct}/{len(invoices)} ({100*correct/len(invoices):.1f}%)")
    print(f"Dangerous errors:  {dangerous} (HIGH confidence but wrong)")
    print(f"Full results:      smith.langchain.com")


if __name__ == "__main__":
    main()
