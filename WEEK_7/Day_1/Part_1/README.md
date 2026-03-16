# LLM as Judges Lab - Week 7

**Student:** Pedro Biain  
**Date:** March 16, 2026  
**Scenario:** Retail Customer Service Chatbot (Option C)

## Lab Overview

This lab completed the full evaluation design process for a retail customer service chatbot, covering benchmark auditing, custom evaluation design, LLM-as-judge implementation, and professional reporting.

## Completed Deliverables

### Part 1: Benchmark Audit & Evaluation Design ✅

**Step 1: Client Scenario** → `client_scenario.md`
- Chose Option C: Retail Customer Service Chatbot
- Key concerns: Policy enforcement, customer satisfaction, safety escalation

**Step 2: Benchmark Audit** → `benchmark_audit.md`
- Evaluated 3 benchmarks: MT-Bench, HELM, ToxiGen
- Assessed contamination risk, saturation risk, and relevance
- Verdict: 2 adapted, 1 rejected

**Step 3: Custom Evaluation Prompts** → `evaluation_design.md` (first section)
- 5 custom prompts designed:
  1. Out-of-policy return (45 days vs 30-day policy) - Rule-based verification
  2. Defective product without receipt - LLM-as-judge
  3. Product compatibility (Samsung/iPhone) - LLM-as-judge
  4. Price match edge case (third-party seller) - Rule-based verification
  5. Harassment complaint escalation - LLM-as-judge ⭐ CRITICAL
- Each includes: ground truth, verification method, failure mode, rationale

**Step 4: Judge Design** → `evaluation_design.md` (second section)
- Complete LLM-as-judge prompt for Prompt #5 (Harassment Complaint)
- Components:
  - Task Description
  - 5 Evaluation Criteria (4 Critical, 1 Important)
  - 5 Reasoning Steps
  - JSON Output Format with scoring rubric (0-5)
  - Bias Analysis (5 identified biases with mitigation strategies)
  - Calibration Strategy (6 reference examples, 4-phase process, success metrics)

**Step 5: Evaluation Memo** → `evaluation_memo.md`
- Professional 1-page memo (expanded to ~2,200 words for completeness)
- Sections:
  - Executive Summary
  - Methodology (models tested, evaluation approach)
  - Results (performance comparison: Claude Sonnet 4, GPT-4o, Gemini 1.5 Pro)
  - Caveats & Limitations (7 critical limitations identified)
  - Recommendation (Claude Sonnet 4 with 5 deployment conditions)
  - Additional Metrics (cost, ROI, environmental impact)

**Step 6: Reflection Questions** → `reflection.md`
- Question 1: French language evaluation challenges
  - Benchmark adaptation, cultural norms, LLM-judge reliability
- Question 2: "Is this AGI?" client question
  - Reframing buzzwords, what models can/can't do, appropriate caveats
- Question 3: What requires human evaluation?
  - Cultural appropriateness, edge cases, hybrid evaluation pipeline

### Part 2: Implementation & Execution (Not Started)

**Step 7-11:** Python implementation, test dataset, evaluation run, results analysis
- Status: TO DO
- Will implement LLM-as-judge for Prompt #5 using OpenAI or LangChain

## Key Learning Points

1. **Evaluation is more than accuracy** - Requires cultural awareness, safety considerations, and legal compliance
2. **Hedging language is critical** - "Under these conditions", "we cannot guarantee", "does not ensure"
3. **Bias in judges** - Even automated judges have cultural assumptions and limitations
4. **Calibration is essential** - Reference examples + human validation + continuous monitoring
5. **Human evaluation irreplaceable** - For contextual nuance, cultural competence, edge cases

## Files in This Folder

- `client_scenario.md` - Retail chatbot scenario description
- `benchmark_audit.md` - 3 benchmark evaluation cards
- `evaluation_design.md` - 5 prompts + complete judge design with bias analysis
- `evaluation_memo.md` - Professional evaluation report with recommendations
- `reflection.md` - 3 reflection questions with detailed answers
- `README.md` - This file

## Next Steps

1. Set up Python environment (OpenAI API or LangChain)
2. Implement judge prompt from `evaluation_design.md`
3. Create test dataset (3-5 examples)
4. Run evaluation and collect metrics
5. Analyze results and create summary

## Notes

- All Part 1 deliverables completed ✅
- Ready to proceed to Python implementation (Part 2)
- Estimated time for Part 2: 60 minutes
