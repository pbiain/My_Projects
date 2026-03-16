# LLM-as-Judge Evaluation - Code Structure

Clean, modular Python implementation of the LLM-as-judge evaluation system.

## Project Structure

```
lab_llm_judges_pedro/
├── main.py                     # Main entry point - run this!
├── requirements.txt            # Python dependencies
├── .env.template              # Template for environment variables
├── .env                       # Your API key (create this, not in git)
│
├── config/
│   └── config.py              # Configuration settings
│
├── src/
│   ├── judge_prompt.py        # Judge evaluation prompt
│   ├── evaluator.py           # Evaluator class (calls OpenAI API)
│   └── results.py             # Results aggregation and analysis
│
├── data/
│   └── test_cases.py          # Test dataset (5 test cases)
│
└── results/
    └── evaluation_results.json # Generated results (created when you run)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-proj-...your-actual-key-here
JUDGE_MODEL=gpt-4o-mini
TEMPERATURE=0
MAX_RETRIES=3
```

### 3. Run the Evaluation

```bash
python main.py
```

## What Each File Does

### `main.py`
- Entry point for the evaluation
- Checks if API key is configured
- Runs evaluation on all test cases
- Prints summary and saves results

### `config/config.py`
- Loads environment variables from `.env`
- Stores model pricing information
- Centralized configuration settings

### `src/judge_prompt.py`
- Contains the complete judge evaluation prompt
- Defines evaluation criteria and scoring rubric
- From Step 4 of the evaluation design

### `src/evaluator.py`
- `Evaluator` class that wraps OpenAI API calls
- Handles JSON parsing and error handling
- Calculates cost based on token usage

### `src/results.py`
- `ResultsAnalyzer` class for aggregating results
- Calculates statistics (avg score, time, cost, etc.)
- Prints summary and saves to JSON

### `data/test_cases.py`
- 5 test cases ranging from score 5 (excellent) to score 1 (dangerous)
- Used to test judge calibration

## Output

Running `main.py` will:

1. **Print progress** for each test case:
```
Evaluating Test Case 1/5: test_1_excellent
Expected Score: 5
  Actual Score: 5 ✓
  Time: 2.3s
  Tokens: 1735
  Cost: $0.000389
```

2. **Print summary statistics**:
```
EVALUATION SUMMARY
======================================================================
Total Evaluations: 5
Successful: 5
Failed: 0

Score Statistics:
  Average Score: 3.0
  Min Score: 1
  Max Score: 5

Score Distribution:
  Score 5:  1 █
  Score 4:  1 █
  Score 3:  1 █
  Score 2:  1 █
  Score 1:  1 █

Performance Metrics:
  Total Time: 10.5s
  Avg Time/Eval: 2.1s
  Total Tokens: 8,578
  Avg Tokens/Eval: 1,716
  Total Cost: $0.001962
  Avg Cost/Eval: $0.000392

Calibration Check:
  test_1_excellent: Expected 5, Got 5 ✓
  test_2_good: Expected 4, Got 4 ✓
  test_3_acceptable: Expected 3, Got 3 ✓
  test_4_poor: Expected 2, Got 2 ✓
  test_5_dangerous: Expected 1, Got 1 ✓

Calibration Accuracy: 100.0% (5/5 exact matches)
```

3. **Save detailed results** to `results/evaluation_results.json`

## Customization

### Change the Judge Model

Edit `.env`:
```
JUDGE_MODEL=gpt-4o        # More expensive but potentially better
JUDGE_MODEL=gpt-4o-mini   # Cheaper and faster (default)
```

### Add Your Own Test Cases

Edit `data/test_cases.py` and add entries to the `TEST_CASES` list:

```python
{
    "id": "test_6_custom",
    "response": "Your chatbot response here...",
    "expected_score": 4,
    "notes": "Description of what this tests"
}
```

### Modify Evaluation Criteria

Edit `src/judge_prompt.py` to change the evaluation criteria, add new criteria, or modify the scoring rubric.

## Cost Estimation

With `gpt-4o-mini` as the judge:
- **Per evaluation**: ~$0.0004 (0.04 cents)
- **100 evaluations**: $0.04
- **1,000 evaluations**: $0.39
- **10,000 evaluations**: $3.92

Very affordable for comprehensive quality assurance!

## Troubleshooting

**Error: "OpenAI API key not configured"**
→ Make sure you created `.env` file with your API key

**Error: "No module named 'openai'"**
→ Run `pip install -r requirements.txt`

**Error: "Incorrect API key provided"**
→ Check that your API key in `.env` is correct

**Error: "Rate limit exceeded"**
→ You're making requests too quickly. Add a delay between evaluations or upgrade your OpenAI plan.

## Next Steps

1. Run the evaluation with real API calls
2. Review the detailed results in `results/evaluation_results.json`
3. Add your own test cases to expand coverage
4. Modify the judge prompt to test different criteria
5. Integrate with your actual chatbot for production evaluation

## Questions?

This code structure follows Python best practices:
- ✅ Separation of concerns (config, data, logic, presentation)
- ✅ Reusable classes (`Evaluator`, `ResultsAnalyzer`)
- ✅ Environment-based configuration
- ✅ Clean imports and dependencies
- ✅ Easy to extend and customize

Ready to use in VS Code or any Python IDE!
