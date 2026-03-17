# Lab: Custom Dataset Creation & Evaluation with LangSmith
**Student:** Pedro Biais  
**Bootcamp:** IronHack AI Engineering — Week 7, Day 2  
**Date:** March 2026

---

## Domain & Dataset
**Domain:** Formula 1 motorsport knowledge Q&A

**Dataset:** `f1-knowledge-qa-v1` — 15 hand-crafted examples across 4 categories:
- Rules & Regulations
- History
- Teams & Drivers
- Race Strategy

Each example contains a question (input) and a reference answer (output), 
with metadata for category and difficulty (easy/medium/hard).

**LangSmith Dataset:**  
`https://eu.smith.langchain.com` → Datasets → `f1-knowledge-qa-v1`

---

## Approach

### Target Function
- Model: `gpt-4o-mini` (temperature=0)
- System prompt: F1 specialist analyst persona
- Tracing: enabled via `@traceable` decorator

### Evaluators
1. **Correctness** — openevals LLM-as-judge using `CORRECTNESS_PROMPT`
2. **F1 Terminology** — custom LLM-as-judge measuring domain-specific 
   language precision (independent of factual correctness)

### Experiments Run
| Experiment | Model | Evaluators |
|------------|-------|------------|
| `f1-gpt4o-mini` | gpt-4o-mini | correctness |
| `f1-gpt4o-mini-dual-eval` | gpt-4o-mini | correctness + terminology |
| `f1-gpt4o` | gpt-4o | correctness + terminology |

---

## Key Results

| Model | Correctness | Terminology | Est. Cost/10K queries |
|-------|-------------|-------------|----------------------|
| gpt-4o-mini | 0.867 | 1.000 | ~$9/day |
| gpt-4o | 0.867 | 1.000 | ~$150/day |

**Main finding:** Both models score identically in aggregate but fail on 
*different* questions. gpt-4o has more recent knowledge (Ferrari HP 
sponsorship) but hallucinated on a simple factual question that mini 
answered correctly. At 16x the cost, gpt-4o offers no aggregate advantage 
on this dataset.

**Recommendation:** gpt-4o-mini + RAG over current F1 documentation is 
the optimal production architecture.

---

## Repository Structure
```
lab_langsmith_pedro/
├── lab_langsmith.ipynb        # Main notebook with all cells
├── f1_evaluation_report.md    # Mandatory evaluation report
├── f1_optimization_report.md  # A/B cost-performance report
└── README.md                  # This file
```

---

## How to Run

1. Clone the repo and activate the environment:
```bash
conda activate ironhack_env
```

2. Create a `.env` file in the project folder:
```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
LANGSMITH_PROJECT=f1-eval
LANGSMITH_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

3. Open `lab_langsmith.ipynb` and run all cells in order

> ⚠️ Cell 4 will skip dataset creation if `f1-knowledge-qa-v1` already 
> exists in LangSmith to avoid duplicates.

---

## LangSmith Links

https://eu.smith.langchain.com/o/a402e573-eccd-453f-bb5b-03465f760fed/datasets/b8b3e282-352e-45ee-9c1e-d8155668403e?tab=0

- **Experiment 1:** f1-gpt4o-mini (correctness only)  
- **Experiment 2:** f1-gpt4o-mini-dual-eval (correctness + terminology)  
- **Experiment 3:** f1-gpt4o (A/B comparison)
- **Dataset:** `f1-knowledge-qa-v1`
- **Project:** `f1-eval`
- **Region:** EU (`eu.smith.langchain.com`)