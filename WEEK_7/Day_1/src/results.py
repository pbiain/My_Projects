"""
ResultsAnalyzer — accumulates evaluation results, computes statistics,
prints summaries, and saves outputs to JSON.
"""

import json
import statistics
from datetime import datetime


class ResultsAnalyzer:
    def __init__(self):
        self._results = []
        self._summary = {}

    def add_result(self, test_case: dict, evaluation: dict):
        """Store a single evaluation result paired with its test case metadata."""
        self._results.append({
            "test_case_id": test_case["id"],
            "category": test_case.get("category", ""),
            "expected_score": test_case["expected_score"],
            "evaluation": evaluation,
        })

    def calculate_statistics(self, judge_model: str):
        """Compute aggregate statistics across all completed evaluations."""
        valid = [
            r for r in self._results
            if "error" not in r["evaluation"]
        ]

        if not valid:
            self._summary = {"error": "No valid results to summarize"}
            return

        actual_scores = [r["evaluation"]["score"] for r in valid]
        expected_scores = [r["expected_score"] for r in valid]
        costs = [r["evaluation"]["metadata"]["estimated_cost_usd"] for r in valid]
        tokens = [r["evaluation"]["metadata"]["total_tokens"] for r in valid]

        exact_matches = sum(
            1 for a, e in zip(actual_scores, expected_scores) if a == e
        )
        within_one = sum(
            1 for a, e in zip(actual_scores, expected_scores) if abs(a - e) <= 1
        )
        pass_count = sum(1 for s in actual_scores if s >= 3)

        self._summary = {
            "judge_model": judge_model,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_cases": len(self._results),
            "valid_cases": len(valid),
            "failed_cases": len(self._results) - len(valid),
            "scores": {
                "mean": round(statistics.mean(actual_scores), 2),
                "median": statistics.median(actual_scores),
                "stdev": round(statistics.stdev(actual_scores), 2) if len(actual_scores) > 1 else 0,
                "min": min(actual_scores),
                "max": max(actual_scores),
            },
            "accuracy": {
                "exact_match": exact_matches,
                "exact_match_pct": round(exact_matches / len(valid) * 100, 1),
                "within_one": within_one,
                "within_one_pct": round(within_one / len(valid) * 100, 1),
            },
            "pass_rate": {
                "passed": pass_count,
                "total": len(valid),
                "pct": round(pass_count / len(valid) * 100, 1),
            },
            "cost": {
                "total_usd": round(sum(costs), 6),
                "mean_per_case_usd": round(statistics.mean(costs), 6),
                "total_tokens": sum(tokens),
            },
        }

    def print_summary(self):
        """Print a human-readable summary to stdout."""
        if not self._summary:
            print("No summary available. Call calculate_statistics() first.")
            return

        if "error" in self._summary:
            print(f"Summary error: {self._summary['error']}")
            return

        s = self._summary
        print(f"\n{'='*70}")
        print("EVALUATION SUMMARY")
        print(f"{'='*70}")
        print(f"Judge Model  : {s['judge_model']}")
        print(f"Timestamp    : {s['timestamp']}")
        print(f"Total Cases  : {s['total_cases']}  (valid: {s['valid_cases']}, failed: {s['failed_cases']})")
        print()
        print("Scores")
        sc = s["scores"]
        print(f"  Mean   : {sc['mean']}   Median : {sc['median']}   StdDev : {sc['stdev']}")
        print(f"  Range  : {sc['min']} – {sc['max']}")
        print()
        print("Accuracy vs. Expected")
        ac = s["accuracy"]
        print(f"  Exact match  : {ac['exact_match']}/{s['valid_cases']} ({ac['exact_match_pct']}%)")
        print(f"  Within ±1    : {ac['within_one']}/{s['valid_cases']} ({ac['within_one_pct']}%)")
        print()
        pr = s["pass_rate"]
        print(f"Pass Rate (score >= 3): {pr['passed']}/{pr['total']} ({pr['pct']}%)")
        print()
        co = s["cost"]
        print(f"Cost")
        print(f"  Total   : ${co['total_usd']:.6f}")
        print(f"  Per case: ${co['mean_per_case_usd']:.6f}")
        print(f"  Tokens  : {co['total_tokens']}")
        print(f"{'='*70}")

    def save_to_file(self, path: str):
        """Save full results + summary to a JSON file."""
        output = {
            "summary": self._summary,
            "results": self._results,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {path}")
