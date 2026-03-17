
# F1 Knowledge Q&A — Evaluation Report
**Model:** gpt-4o-mini  
**Dataset:** f1-knowledge-qa-v1 (15 examples)  
**Evaluator:** LLM-as-judge correctness (openevals)  
**Date:** March 2026

---

## Executive Summary
gpt-4o-mini achieved a correctness score of **0.867 (13/15)** on a custom F1 
knowledge dataset spanning rules, history, teams/drivers, and race strategy.
Performance was strong across stable knowledge domains but degraded on 
recent or sponsorship-specific facts.

---

## Methodology
- **Dataset:** 15 hand-crafted Q&A examples across 4 categories and 3 
  difficulty levels (easy/medium/hard)
- **Target function:** gpt-4o-mini with temperature=0 and an F1-specialist 
  system prompt
- **Evaluator:** LLM-as-judge using openevals CORRECTNESS_PROMPT, 
  graded by gpt-4o-mini
- **Infrastructure:** LangSmith (EU region) for tracing, dataset management, 
  and experiment tracking

---

## Results

### Overall
| Metric | Value |
|--------|-------|
| Mean correctness | 0.867 |
| Examples passed | 13/15 |
| P50 Latency | 4.22s |
| P99 Latency | 8.17s |

### By Category
| Category | Correct | Total | Accuracy |
|----------|---------|-------|----------|
| Rules | 4 | 4 | 100% |
| Strategy | 4 | 4 | 100% |
| History | 3 | 4 | 75% |
| Teams & Drivers | 2 | 3 | 67% |

### By Difficulty
| Difficulty | Correct | Total | Accuracy |
|------------|---------|-------|----------|
| Medium | 7 | 7 | 100% |
| Easy | 6 | 7 | 86% |
| Hard | 0 | 1 | 0% |

---

## Failed Examples
1. **[history / easy]** "Which constructor has won the most F1 Constructors' 
   Championships?" — Model likely returned an incorrect count or named the 
   wrong team.
2. **[teams_drivers / hard]** "What is the name of Ferrari's F1 team in 
   official FIA documentation and why?" — The HP sponsorship suffix is 
   post-training cutoff knowledge; the model could not be expected to know this.

---

## Analysis
**Strengths:**
- Perfect accuracy on rules and strategy questions — these are well-documented, 
  stable facts that are well-represented in training data
- Strong medium-difficulty performance (100%) suggests the model handles 
  nuanced F1 concepts reliably
- Low latency (P50 4.22s) makes it viable for real-time applications

**Weaknesses:**
- Recent or sponsorship-specific facts (Ferrari HP) fall outside the model's 
  training cutoff — a RAG approach over current F1 documentation would fix this
- Historical stats (constructor titles) show occasional hallucination even on 
  "easy" questions — these should be grounded with retrieval

---

## Limitations
- Dataset size is small (15 examples) — results may not generalise broadly
- LLM-as-judge evaluator uses the same model family as the target, which may 
  introduce leniency bias
- Single evaluation run — variance across runs not measured

---

## Recommendations
1. **Add RAG** over current F1 documentation for team/sponsorship facts
2. **Expand dataset** to 50+ examples for statistical reliability
3. **Compare gpt-4o vs gpt-4o-mini** to quantify the cost/performance gap
   (covered in Optional Part 2)
4. **Custom evaluator** for F1 terminology accuracy beyond binary correctness
   (covered in Optional Part 1)
