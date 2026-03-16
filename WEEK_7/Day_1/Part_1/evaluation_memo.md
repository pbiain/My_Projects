# Evaluation Memo

---

**TO:** Sarah Martinez, VP of Customer Experience, RetailCo  
**FROM:** Pedro Biain, AI Evaluation Consultant  
**DATE:** March 16, 2026  
**SUBJECT:** Customer Service Chatbot Evaluation Results - Harassment Complaint Handling

---

## EXECUTIVE SUMMARY

We evaluated three leading LLM models (GPT-4o, Claude Sonnet 4, and Gemini 1.5 Pro) on their ability to handle sensitive customer service scenarios for RetailCo's planned chatbot deployment. The evaluation focused on five critical scenarios: policy enforcement, complaint handling, product knowledge accuracy, edge case navigation, and safety escalation. Under controlled test conditions, Claude Sonnet 4 demonstrated the strongest performance in appropriately escalating harassment complaints while maintaining policy compliance, though all models showed areas requiring refinement before production deployment.

---

## METHODOLOGY

### Evaluation Approach

We designed a custom evaluation framework specifically for RetailCo's customer service chatbot use case, focusing on scenarios identified as high-risk during our discovery phase. The evaluation consisted of five test prompts covering:

1. **Policy Enforcement** - Out-of-policy return request (45-day return vs. 30-day policy)
2. **Complaint Handling** - Defective product without receipt
3. **Knowledge Accuracy** - Product compatibility questions (Samsung/iPhone compatibility)
4. **Edge Case Navigation** - Price match with third-party seller exclusions
5. **Safety Escalation** - Harassment complaint requiring human intervention

For evaluation, we used a combination of rule-based verification (for policy compliance prompts) and LLM-as-judge methodology (for nuanced scenarios requiring assessment of empathy, tone, and escalation appropriateness). The judge was calibrated using six reference examples spanning scores from 0 (catastrophic failure) to 5 (excellent response).

### Models Tested

- **GPT-4o** (OpenAI, gpt-4o-2024-08-06)
- **Claude Sonnet 4** (Anthropic, claude-sonnet-4-20250514)
- **Gemini 1.5 Pro** (Google, gemini-1.5-pro-002)

All models were tested using identical prompts with temperature=0.7 to balance consistency with natural response variation. Each prompt was run three times per model to assess response variance.

### Evaluation Criteria

For the harassment complaint scenario (our highest-risk test case), responses were evaluated on five criteria:

1. **Seriousness & Empathy** (Critical) - Takes complaint seriously without minimizing
2. **Escalation Commitment** (Critical) - Clear, specific escalation to HR/management
3. **Liability Avoidance** (Critical) - No promises about employee discipline
4. **Scope Recognition** (Critical) - Defers to human judgment appropriately
5. **Tone & Professionalism** (Important) - Maintains empathetic but professional tone

Responses were scored 0-5, with scores below 3 considered unacceptable for production deployment.

---

## RESULTS

### Overall Performance Summary

| Model | Harassment Escalation (avg score) | Policy Enforcement (pass rate) | Knowledge Accuracy (pass rate) | Overall Recommendation |
|-------|-----------------------------------|-------------------------------|--------------------------------|----------------------|
| **Claude Sonnet 4** | 4.7/5 | 100% (3/3) | 100% (3/3) | **Recommended with refinements** |
| **GPT-4o** | 4.3/5 | 100% (3/3) | 67% (2/3) | Acceptable alternative |
| **Gemini 1.5 Pro** | 3.0/5 | 67% (2/3) | 100% (3/3) | Not recommended |

### Key Findings by Scenario

**Scenario 1: Policy Enforcement (Out-of-policy Return)**

All three models successfully enforced the 30-day return policy when presented with a 45-day return request. Claude Sonnet 4 and GPT-4o maintained empathetic tone while declining the request, offering alternatives (store credit, manager escalation). Gemini 1.5 Pro in one trial incorrectly approved the return, citing the customer's claim that "store staff said it was possible" as justification—a critical failure in policy adherence.

**Scenario 2: Complaint Handling (Defective Product)**

All models appropriately offered store credit (not refund) for defective products without receipt, as per policy. Claude Sonnet 4 excelled at balancing empathy with policy enforcement, consistently de-escalating the angry customer while maintaining boundaries. GPT-4o occasionally used slightly more formal language that could feel less empathetic. Gemini 1.5 Pro responses were adequate but lacked proactive helpfulness (e.g., offering to check purchase history via payment method).

**Scenario 3: Knowledge Accuracy (Product Compatibility)**

Claude Sonnet 4 and Gemini 1.5 Pro correctly explained that Samsung Galaxy Buds Pro 2 work with iPhone 13 via Bluetooth but with feature limitations. GPT-4o in one trial hallucinated that "full features work on any device," a factually incorrect claim that could lead to customer dissatisfaction and returns. This highlights the ongoing challenge of factual accuracy in LLM responses.

**Scenario 4: Edge Case Navigation (Price Match)**

Claude Sonnet 4 and GPT-4o correctly identified that third-party marketplace sellers don't qualify for price matching and explained this clearly while maintaining customer engagement. Gemini 1.5 Pro correctly applied the policy but responses felt more transactional, missing opportunities to offer alternative value propositions (loyalty points, warranties, etc.).

**Scenario 5: Safety Escalation (Harassment Complaint)** ⭐ **CRITICAL TEST**

This scenario tested the most high-stakes situation: a customer reporting employee harassment.

**Claude Sonnet 4 (Score: 4.7/5):**
- Consistently took complaints seriously with appropriate empathy
- Explicitly escalated to "HR department and store management"
- Avoided all liability-creating promises about employee discipline
- Provided specific next steps (24-48 hour contact timeline)
- Minor improvement area: Could be more specific about contact information in 1 of 3 trials

**GPT-4o (Score: 4.3/5):**
- Validated customer feelings and showed empathy
- Clear escalation commitment in all trials
- No liability issues detected
- Slightly less specific on escalation contacts ("management team" vs. "HR and Store Manager")
- Tone occasionally felt slightly formal

**Gemini 1.5 Pro (Score: 3.0/5):**
- Met basic escalation requirement but with concerning weaknesses
- In 1 of 3 trials, used language that could be interpreted as minimizing ("we'll look into this")
- Escalation was present but vague ("appropriate department" vs. specific HR/management)
- Lacked specificity on next steps and timeline
- Tone was professional but less empathetic than competitors

### Performance Metrics Beyond Accuracy

| Metric | Claude Sonnet 4 | GPT-4o | Gemini 1.5 Pro |
|--------|----------------|---------|----------------|
| **Avg Response Time** | 2.1 seconds | 1.8 seconds | 2.4 seconds |
| **Avg Tokens Used** | 187 tokens | 203 tokens | 165 tokens |
| **Estimated Cost per 1000 interactions** | $3.74 | $5.06 | $2.48 |
| **Response Variance (consistency)** | Low | Low | Medium |

*Note: Costs based on current API pricing as of March 2026. Production costs may vary with volume discounts.*

---

## CAVEATS & LIMITATIONS

### What We Cannot Guarantee

**1. Real-World Performance Variability**

This evaluation was conducted on five carefully designed test prompts under controlled conditions. Real customer interactions will be far more diverse, ambiguous, and unpredictable. The models' performance on our test set does not guarantee equivalent performance across all possible customer service scenarios RetailCo may encounter.

**2. Benchmark Contamination & Training Data**

We cannot verify what training data these models were exposed to. It is possible that similar customer service scenarios exist in their training sets, which could inflate performance scores. Our custom prompts were designed to be novel, but we cannot rule out some degree of pattern recognition rather than genuine reasoning.

**3. Evaluation Scope Limitations**

Our evaluation focused on text-based accuracy, policy compliance, and tone. We did NOT evaluate:
- Multi-turn conversation handling (our prompts were single-turn)
- Response to adversarial customer inputs or jailbreak attempts
- Performance degradation over long conversations
- Handling of non-English interactions or multilingual code-switching
- Edge cases involving protected characteristics (age, disability, race, etc.)

**4. Temporal Consistency Not Assessed**

LLM outputs can vary even with identical inputs due to model updates, API changes, or inherent randomness (even at temperature=0.7, some variance exists). We ran each prompt three times to assess variance, but longer-term consistency (weeks or months of production use) was not evaluated.

**5. Judge Reliability**

For subjective criteria (empathy, tone), we used an LLM-as-judge approach with Claude Sonnet 4 as the evaluator. This introduces potential biases:
- The judge may favor responses similar to its own communication style
- Cultural assumptions embedded in the judge (Western corporate norms around HR escalation)
- Potential conflicts of interest when Claude judges its own responses (though we used a separate instance with no access to the evaluated outputs)

We calibrated the judge using reference examples and validated against human judgment on a subset, achieving 87% agreement within ±1 point. However, this is not perfect alignment.

**6. Cost Estimates Are Approximate**

Token usage and costs were measured on our specific test prompts. Production costs will vary based on:
- Actual conversation length (our tests were concise prompts)
- System prompt overhead (not included in our measurements)
- Volume-based API pricing tiers
- Potential need for retry logic or fallback models

**7. Safety Evaluation Incompleteness**

While we tested one harassment scenario, comprehensive safety evaluation would require:
- Adversarial testing (attempts to make the model generate harmful content)
- Testing across protected categories (race, religion, gender, etc.)
- Evaluation of potential discriminatory patterns in responses
- Testing refusal behaviors when asked to violate policies

This evaluation focused on "happy path" safety (correct handling of legitimate complaints), not adversarial robustness.

---

## RECOMMENDATION

### Primary Recommendation: Claude Sonnet 4

**For RetailCo's customer service chatbot deployment, we recommend Claude Sonnet 4** under the following conditions:

**Strengths:**
- Highest performance on critical safety scenario (harassment escalation): 4.7/5
- Perfect policy compliance across all scenarios tested
- Best balance of empathy and professionalism
- Most consistent responses across multiple runs
- Strong performance on knowledge accuracy

**Use Cases Where This Model Excels:**
- High-stakes customer interactions requiring empathy and escalation judgment
- Policy enforcement scenarios requiring nuanced explanations
- Situations where customer retention and satisfaction are balanced with business rules

**Conditions for Deployment:**
1. **Human-in-the-loop for harassment complaints**: Despite strong performance, all harassment/safety complaints should trigger immediate human review
2. **Knowledge base integration required**: Product compatibility and technical questions should pull from verified knowledge base, not rely solely on model knowledge
3. **Continuous monitoring**: Implement sampling-based human review (recommend 5% of interactions) to catch edge cases
4. **Clear escalation triggers**: Define explicit rules for when chatbot hands off to human agents
5. **Regular re-evaluation**: Re-run evaluations quarterly to ensure performance doesn't degrade with model updates

**Cost Consideration:**
At $3.74 per 1,000 interactions, Claude Sonnet 4 is mid-range in cost but offers the best risk-adjusted value given the high stakes of customer-facing interactions in retail.

### Alternative Option: GPT-4o

GPT-4o is an acceptable alternative if cost is the primary concern ($5.06 per 1,000 interactions makes it the most expensive option, which may not align with RetailCo's budget constraints). 

**Key Difference:**
- Slightly lower harassment escalation score (4.3 vs 4.7)
- One knowledge accuracy failure (hallucinated full compatibility)
- Faster response time (1.8s vs 2.1s)

**When to choose GPT-4o over Claude:**
- If response speed is critical (sub-2-second requirement)
- If cost difference is negligible at RetailCo's projected volume
- If integration with existing OpenAI infrastructure is significantly easier

### Not Recommended: Gemini 1.5 Pro

While Gemini 1.5 Pro showed perfect knowledge accuracy and is the most cost-effective option ($2.48 per 1,000 interactions), its performance on critical safety scenarios (score 3.0/5 on harassment escalation) and policy enforcement failures (1 of 3 trials incorrectly approved out-of-policy return) make it unsuitable for customer-facing deployment at this time.

**Potential Use Case for Gemini:**
Could be considered for lower-stakes internal tools or as a fallback model for simple FAQ-style queries where safety escalation is not a factor.

---

## ADDITIONAL METRICS

### Environmental & Operational Considerations

**Carbon Footprint Estimate:**
Based on token usage and estimated compute requirements:
- Claude Sonnet 4: ~0.12g CO2e per interaction
- GPT-4o: ~0.15g CO2e per interaction  
- Gemini 1.5 Pro: ~0.10g CO2e per interaction

*At RetailCo's projected 100,000 interactions/month, this translates to approximately 12-15kg CO2e/month. This is comparable to ~60-75 miles driven in a gasoline vehicle.*

### Scalability & Latency

All three models demonstrated acceptable latency for customer service applications (under 3 seconds average response time). At projected peak load (500 concurrent conversations), all three providers have confirmed capacity to handle RetailCo's volume without degradation.

**Reliability SLAs:**
- Anthropic (Claude): 99.9% uptime SLA
- OpenAI (GPT-4o): 99.9% uptime SLA  
- Google (Gemini): 99.95% uptime SLA

### Cost-Benefit Analysis

**Estimated Annual Costs (at 1.2M interactions/year):**
- Claude Sonnet 4: $4,488/year
- GPT-4o: $6,072/year
- Gemini 1.5 Pro: $2,976/year

**Projected Customer Service Cost Savings:**
Implementing a chatbot handling 60% of Tier 1 inquiries (estimated 720K interactions/year) could reduce human agent workload by approximately 14,400 hours/year. At an average fully-loaded agent cost of $25/hour, this represents $360,000 in annual savings.

**ROI Calculation:**
Even with the highest-cost option (GPT-4o at $6,072/year), the projected ROI is approximately 5,900% in Year 1, with payback period under 1 week. Cost differences between models ($3,096 annual variance) are negligible compared to operational savings.

**However**, this analysis assumes no significant failures requiring human intervention beyond planned escalation. A single serious mishandling of a harassment complaint could result in legal costs, reputational damage, and customer attrition far exceeding annual operating costs. **Therefore, model quality and safety performance are more important selection criteria than per-interaction cost.**

---

## NEXT STEPS

1. **Stakeholder Review** (Week of March 18): Present findings to Customer Experience and Legal teams
2. **Pilot Deployment** (April 2026): Deploy Claude Sonnet 4 to 5% of web chat traffic with 100% human review
3. **Monitoring Framework** (April-May 2026): Establish metrics dashboard and weekly review cadence
4. **Phased Rollout** (June 2026): Increase to 25% traffic if pilot metrics meet targets
5. **Quarterly Re-evaluation** (July 2026): Re-run evaluation suite to ensure continued performance

---

**Contact for Questions:**  
Pedro Biain  
AI Evaluation Consultant  
pedro@example.com
