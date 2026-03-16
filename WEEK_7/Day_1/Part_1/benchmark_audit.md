# Benchmark Audit

## Benchmark 1: MT-Bench (Multi-Turn Benchmark)

**Benchmark Name:** MT-Bench  
**Year:** 2023  
**Source:** https://arxiv.org/abs/2306.05685

**Why it seemed relevant:**
MT-Bench evaluates multi-turn conversation capabilities across various categories including writing, roleplay, reasoning, and extraction. Since our retail chatbot needs to handle multi-turn conversations with customers (clarifying questions, follow-ups), this benchmark tests the model's ability to maintain context and provide coherent responses across dialogue turns.

**Contamination risk:**
- [X] Medium - Some overlap possible
- **Explanation:** MT-Bench was released in 2023 and has become widely used. Many modern models (GPT-4, Claude, etc.) may have been fine-tuned on similar conversational patterns, though the specific prompts may not have been in training data.

**Saturation risk:**
- [X] Medium - Some models perform well
- **Explanation:** Top-tier models (GPT-4, Claude 3) score well on MT-Bench, but there's still differentiation between models. Mid-tier models show clear performance gaps.

**Format:**
- [X] Free-form text
- Multi-turn conversational format with judge evaluation

**Verdict:**
- [X] Adapt it
- **How:** Use the multi-turn conversation structure but create retail-specific scenarios (product inquiries, return requests, complaint handling). Keep the judge-based evaluation approach but customize evaluation criteria for retail customer service (helpfulness, tone, accuracy, resolution).

---

## Benchmark 2: HELM - Summarization & Question Answering

**Benchmark Name:** HELM (Holistic Evaluation of Language Models) - Summarization & QA scenarios  
**Year:** 2022  
**Source:** https://crfm.stanford.edu/helm/

**Why it seemed relevant:**
HELM includes scenarios for summarization and question answering which are relevant for a retail chatbot that needs to extract information from product descriptions, FAQs, and policies, then provide clear answers to customer questions. The benchmark evaluates accuracy, relevance, and coherence.

**Contamination risk:**
- [X] High - Model definitely saw this during training
- **Explanation:** HELM uses well-known datasets (CNN/DailyMail for summarization, SQuAD for QA) that were available before most modern LLMs were trained. High likelihood of contamination.

**Saturation risk:**
- [X] High - Many models achieve near-perfect scores
- **Explanation:** Modern LLMs perform extremely well on standard summarization and QA tasks. Little differentiation between top models.

**Format:**
- [X] Free-form text
- Question-answer pairs and summarization tasks

**Verdict:**
- [X] Reject it
- **Why:** High contamination and saturation risks make this unsuitable for discriminating between models for our use case. We need fresh, domain-specific evaluation prompts that reflect actual retail scenarios the model hasn't seen during training.

---

## Benchmark 3: ToxiGen

**Benchmark Name:** ToxiGen  
**Year:** 2022  
**Source:** https://arxiv.org/abs/2203.09509

**Why it seemed relevant:**
ToxiGen evaluates models for toxic language generation and implicit hate speech. For a customer-facing chatbot, it's critical that the model doesn't generate inappropriate, offensive, or discriminatory content, especially when handling frustrated or upset customers.

**Contamination risk:**
- [X] Low - Model likely not trained on this data
- **Explanation:** ToxiGen uses adversarially generated examples designed to be challenging and is more recent (2022). Less likely to be directly in training data.

**Saturation risk:**
- [X] Low - Benchmark is challenging
- **Explanation:** Models still struggle with implicit toxicity and edge cases. Good differentiation between models, especially for subtle harmful content.

**Format:**
- [X] Multiple Choice
- Binary classification (toxic vs. non-toxic)

**Verdict:**
- [X] Adapt it
- **How:** Use the toxicity evaluation framework but create retail-specific test cases: responses to angry customers, handling of sensitive topics (refunds, defective products), edge cases with potentially offensive customer messages. Evaluate both whether the model avoids toxic responses AND whether it maintains professionalism under pressure.
