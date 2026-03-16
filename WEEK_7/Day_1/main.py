"""
Main script to run LLM-as-judge evaluation.

Usage:
    python main.py
"""

import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import Evaluator
from src.results import ResultsAnalyzer
from src.judge_prompt import JUDGE_PROMPT
from data.test_cases import TEST_CASES
from config.config import OPENAI_API_KEY, JUDGE_MODEL


def check_api_key():
    """Check if OpenAI API key is configured."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
        print("="*70)
        print("ERROR: OpenAI API key not configured")
        print("="*70)
        print("\nPlease follow these steps:")
        print("1. Copy .env.template to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run this script again")
        print("\nGet your API key from: https://platform.openai.com/api-keys")
        print("="*70)
        return False
    return True


def run_evaluation():
    """Run the complete evaluation suite."""
    
    # Check API key
    if not check_api_key():
        return
    
    print(f"\n{'='*70}")
    print(f"Running LLM-as-Judge Evaluation")
    print(f"Judge Model: {JUDGE_MODEL}")
    print(f"Test Cases: {len(TEST_CASES)}")
    print(f"{'='*70}\n")
    
    # Initialize evaluator and results analyzer
    evaluator = Evaluator(JUDGE_PROMPT)
    analyzer = ResultsAnalyzer()
    
    # Run evaluation on each test case
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Evaluating Test Case {i}/{len(TEST_CASES)}: {test_case['id']}")
        print(f"Expected Score: {test_case['expected_score']}")
        
        # Evaluate
        evaluation = evaluator.evaluate(test_case["response"])
        
        # Add to results
        analyzer.add_result(test_case, evaluation)
        
        # Print result
        if "error" not in evaluation:
            actual_score = evaluation.get("score", 0)
            match = "✓" if actual_score == test_case['expected_score'] else f"✗ (off by {abs(actual_score - test_case['expected_score'])})"
            
            print(f"  Actual Score: {actual_score} {match}")
            print(f"  Time: {evaluation['metadata']['elapsed_time_seconds']}s")
            print(f"  Tokens: {evaluation['metadata']['total_tokens']}")
            print(f"  Cost: ${evaluation['metadata']['estimated_cost_usd']:.6f}")
        else:
            print(f"  ERROR: {evaluation.get('error', 'Unknown error')}")
        
        print()
    
    # Calculate statistics
    analyzer.calculate_statistics(JUDGE_MODEL)
    
    # Print summary
    analyzer.print_summary()
    
    # Save results
    os.makedirs("results", exist_ok=True)
    analyzer.save_to_file("results/evaluation_results.json")
    
    print("\n✓ Evaluation complete!")


if __name__ == "__main__":
    run_evaluation()
