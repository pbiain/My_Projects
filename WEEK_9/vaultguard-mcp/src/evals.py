#!/usr/bin/env python3
"""
Evaluation and testing utilities for VaultGuard MCP Server
"""

import json
import asyncio
from typing import List, Dict, Any
from pathlib import Path

from .invoice_processor import InvoiceProcessor, InvoiceData
from .llm_client import LLMClient


class Evaluator:
    """Evaluation utilities for invoice classification"""

    def __init__(self):
        self.llm_client = LLMClient()
        self.processor = InvoiceProcessor(self.llm_client)

    async def evaluate_accuracy(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate classification accuracy against test cases

        Args:
            test_cases: List of test cases with expected decisions

        Returns:
            Evaluation results
        """
        results = []
        correct = 0
        total = len(test_cases)

        for test_case in test_cases:
            invoice_data = InvoiceData(**test_case["invoice"])
            expected = test_case["expected_decision"]

            # Get prediction
            prediction = await self.processor.classify_invoice(invoice_data)

            # Check if correct
            is_correct = prediction.decision.upper() == expected.upper()
            if is_correct:
                correct += 1

            results.append({
                "invoice_id": invoice_data.invoice_id,
                "expected": expected,
                "predicted": prediction.decision,
                "confidence": prediction.confidence,
                "correct": is_correct,
                "reason": prediction.reason
            })

        accuracy = correct / total if total > 0 else 0

        return {
            "total_cases": total,
            "correct_predictions": correct,
            "accuracy": round(accuracy * 100, 2),
            "results": results
        }

    async def run_evaluation(self, test_file: str = "evals/invoice_examples.json") -> Dict[str, Any]:
        """
        Run evaluation using test cases from file

        Args:
            test_file: Path to test cases JSON file

        Returns:
            Evaluation results
        """
        test_path = Path(__file__).parent.parent / test_file

        if not test_path.exists() or test_path.stat().st_size == 0:
            # Create sample test cases
            sample_cases = [
                {
                    "invoice": {
                        "invoice_id": "TEST-001",
                        "serial_number": "SV100-12345",
                        "safe_age_yr": 3.5,
                        "labour_charge": 186.0,
                        "parts_cost": 0.0,
                        "total_amount": 186.0,
                        "oos_tier1": "Physical Damage",
                        "oos_tier2": "Broken Screen",
                        "comment": "Customer reported screen was smashed",
                        "current_decision": "UNKNOWN"
                    },
                    "expected_decision": "YES"
                },
                {
                    "invoice": {
                        "invoice_id": "TEST-002",
                        "serial_number": "SV200-67890",
                        "safe_age_yr": 5.2,
                        "labour_charge": 186.0,
                        "parts_cost": 45.50,
                        "total_amount": 231.50,
                        "oos_tier1": "Wear and Tear",
                        "oos_tier2": "Validator Spring",
                        "comment": "Validator spring worn out, replaced",
                        "current_decision": "UNKNOWN"
                    },
                    "expected_decision": "NO"
                },
                {
                    "invoice": {
                        "invoice_id": "TEST-003",
                        "serial_number": "SV300-11111",
                        "safe_age_yr": 2.1,
                        "labour_charge": 621.0,
                        "parts_cost": 0.0,
                        "total_amount": 621.0,
                        "oos_tier1": "Software Issue",
                        "oos_tier2": "Firmware Update",
                        "comment": "Remote firmware update required",
                        "current_decision": "UNKNOWN"
                    },
                    "expected_decision": "NO"
                }
            ]

            # Save sample cases
            test_path.parent.mkdir(exist_ok=True)
            with open(test_path, 'w') as f:
                json.dump(sample_cases, f, indent=2)

            print(f"Created sample test cases in {test_path}")

        # Load test cases
        with open(test_path, 'r') as f:
            test_cases = json.load(f)

        # Run evaluation
        results = await self.evaluate_accuracy(test_cases)

        # Print results
        print("\n=== Evaluation Results ===")
        print(f"Total test cases: {results['total_cases']}")
        print(f"Correct predictions: {results['correct_predictions']}")
        print(f"Accuracy: {results['accuracy']}%")

        print("\n=== Detailed Results ===")
        for result in results['results']:
            status = "✓" if result['correct'] else "✗"
            print(f"{status} {result['invoice_id']}: Expected {result['expected']}, Predicted {result['predicted']} ({result['confidence']})")
            if not result['correct']:
                print(f"    Reason: {result['reason']}")

        return results


async def main():
    """Run evaluation"""
    evaluator = Evaluator()
    await evaluator.run_evaluation()


if __name__ == "__main__":
    asyncio.run(main())