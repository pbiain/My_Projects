
# F1 Evaluation — Cost & Performance Optimization Report
**Date:** March 2026  
**Dataset:** f1-knowledge-qa-v1 (15 examples)  
**Evaluators:** correctness + f1_terminology (LLM-as-judge)

---

## Models Tested
| Model | Correctness | Terminology | Cost Input (per 1K tokens) | Cost Output (per 1K tokens) |
|-------|-------------|-------------|----------------------------|-----------------------------|
| gpt-4o-mini | 0.867 | 1.000 | $0.15 | $0.60 |
| gpt-4o | 0.867 | 1.000 | $2.50 | $10.00 |

---

## Key Finding: Equal Performance, 16x Cost Difference
Both models achieved identical aggregate correctness (13/15, 0.867) and 
perfect terminology scores (1.0). However, gpt-4o costs approximately 
16x more on input tokens and 16x more on output tokens.

---

## Per-Example Divergence
The models did NOT fail on the same examples:

| Question | gpt-4o-mini | gpt-4o |
|----------|-------------|--------|
| Ferrari official team name (HP suffix) | ❌ | ✅ |
| Points for winning a race | ✅ | ❌ |

**Interpretation:**
- gpt-4o has more recent knowledge (Ferrari HP sponsorship post-cutoff for mini)
- gpt-4o-mini is more reliable on simple factual questions (points system)
- Neither model is strictly superior — they fail on different question types

---

## Cost-Performance Analysis
For a production F1 knowledge system processing 10,000 queries/day:

| Model | Est. Daily Cost* | Correctness |
|-------|-----------------|-------------|
| gpt-4o-mini | ~$9/day | 86.7% |
| gpt-4o | ~$150/day | 86.7% |

*Estimated at ~200 tokens input + ~150 tokens output per query

---

## Recommendations

**Use gpt-4o-mini when:**
- Budget is a constraint
- Questions focus on rules, strategy, and established history
- High query volume is expected
- Latency matters (faster responses)

**Use gpt-4o when:**
- Maximum knowledge recency is required
- Questions involve recent team/sponsorship changes
- Budget is not a constraint
- Running low-volume, high-stakes evaluations

**Best balanced option:**
- Use gpt-4o-mini as the default with a RAG layer over current F1 
  documentation to cover knowledge cutoff gaps — this would likely push 
  both models to 100% correctness at a fraction of the cost of gpt-4o alone.

---

## Limitations
- 15 examples is too small to draw statistically significant conclusions
- LLM-as-judge uses gpt-4o-mini which may favour its own outputs
- Cost estimates are approximate and exclude evaluator API calls
- A single run per model — variance not measured
