# Prompt Engineering Lab — Final Report
**Student:** Pedro Biain
**Lab:** M2.01 — Prompt Engineering Lab
**Date:** February 2026

---

## 1. Overview

This lab explored prompt engineering techniques for three task types used in a customer service chatbot scenario for TechFlow Solutions. Each task was tested across three prompt versions (v1, v2, v3) with 15 runs each to measure consistency and improvement.

| Task | Technique Applied |
|------|------------------|
| Sentiment Analysis | Few-Shot Examples |
| Product Description | Few-Shot + Structure |
| Data Extraction | Chain-of-Thought (CoT) |

---

## 2. Failure Analysis

### 2.1 Sentiment Analysis

| Version | Success Rate | Unique Responses | Technique |
|---------|-------------|-----------------|-----------|
| v1 (zero-shot) | 0% | 15/15 | No instructions |
| v2 (structured) | 100% | 1-2/15 | Role + labels + max_tokens |
| v3 (few-shot) | 100% | 1/15 | + Few-shot examples |

**Failure Patterns Identified:**
- v1 never returned a clean label — model defaulted to conversational responses
- Root cause: default system message `"You are a helpful assistant"` conflicted with classification task
- Model resolved the conflict by being helpful rather than precise
- Examples of v1 failures:
  - `"That's great to hear! What do you love most about it?"`
  - `"The customer message can be classified as Positive Feedback or Customer Satisfaction"`

**Key Fix:** Aligning the system message to the task role was the single highest-impact change.

---

### 2.2 Product Description

| Version | Success Rate | Avg Words | Std Dev | Technique |
|---------|-------------|-----------|---------|-----------|
| v1 (zero-shot) | 0% | 292 words | ~35 | No instructions |
| v2 (structured) | 100% | 80 words | ~12 | Role + structure + max_tokens |
| v3 (few-shot) | 100% | 57 words | ~8 | + Few-shot example |

**Failure Patterns Identified:**
- v1 showed 100% success at low bar (non-empty response) — **binary pass/fail completely hid the real failures**
- Real failures were in secondary metrics:
  - 292 average words vs 100-word target
  - 15 unique product names invented across 15 runs
  - No consistent structure — some responses had headlines, some didn't
- v1 examples of inconsistency:
  - `Wireless Precision Mouse`, `Wireless Comfort Mouse`, `SwiftClick`, `Wireless Freedom Mouse`

**Key Learning:** For generation tasks, binary pass/fail is a misleading metric. Word count and standard deviation tell the real story.

---

### 2.3 Data Extraction

| Version | Success Rate | Markdown Failures | Technique |
|---------|-------------|-------------------|-----------|
| v1 (zero-shot) | 0% | 15/15 | No format specified |
| v2 (structured) | 100% | 0/15 | Role + fields + no markdown |
| v3 (Chain-of-Thought) | 100% | 0/15 | + CoT reasoning |

**Failure Patterns Identified:**
- v1 failed because model wrapped every JSON response in markdown code fences
- Data extracted was correct — failure was purely formatting
- This is a production failure invisible to human eyes — only caught by testing `json.loads()`
- Secondary issue discovered: without explicit field name format, model returned `"Order ID"` instead of `"order_id"` — breaking downstream parsing

**Key Fix:** Specifying exact snake_case field names in both the prompt and system message eliminated all field name inconsistencies.

---

## 3. Prompt Versions — Final Documentation

### 3.1 Sentiment Analysis v3 (Few-Shot)

```
Classify the sentiment of customer messages.
Respond with exactly one word: Positive, Negative, or Neutral.

Examples:
Message: "This product is amazing, best purchase I've made!"
Label: Positive

Message: "It broke after one day. Complete waste of money."
Label: Negative

Message: "The item arrived on time and was as described."
Label: Neutral

Message: "Terrible experience, I want a refund immediately."
Label: Negative

Now classify this:
Message: "{customer_message}"
Label:
```

**System Message:** `"You are a sentiment classification engine. You only respond with a single word: Positive, Negative, or Neutral. Nothing else."`

**Why it works:**
- Examples show exact capitalisation and no punctuation
- Prompt ends with `Label:` — completion trigger forces a single word continuation
- `max_tokens=5` makes it physically impossible to return more than one word
- 4 examples cover all three labels including a second negative to show variety

---

### 3.2 Product Description v3 (Few-Shot + Structure)

```
Write a product description following this exact format and length.

Example:
Input: Bluetooth headphones, $49.99
Output:
### Crystal Clear Sound on the Go
Immerse yourself in premium audio without the premium price tag.
At $49.99 these headphones deliver studio quality comfort for everyday use.
- Battery: 30-hour playtime on a single charge
- Connectivity: Bluetooth 5.0 with 33ft range
- Comfort: Memory foam ear cushions for all-day wear

Now write one following the exact same format:
Input: {product}, {price}
Output:
```

**System Message:** `"You are a professional product copywriter. You follow the example format exactly — one headline, two sentences, exactly three bullet points. Never exceed 100 words."`

**Why it works:**
- One concrete example anchors length, tone, format, and style simultaneously
- Prompt ends with `Output:` — completion trigger continues the pattern
- `###` headline marker makes validation precise and unambiguous
- Example demonstrates exactly 3 bullets so model copies the count

---

### 3.3 Data Extraction v3 (Chain-of-Thought)

```
Extract data from this customer feedback into clean JSON.

Think through each field step by step before writing your final answer:

Step 1 - order_id: Find any order or item number mentioned.
Step 2 - order_date: Find the date and convert to YYYY-MM-DD format.
         If the year is not mentioned use 2024.
Step 3 - sentiment: Consider ALL positive and negative signals.
         If mixed, lean Neutral.
Step 4 - reported_issues: List only actual problems, not neutral observations.

After your reasoning write your final output as clean JSON using
these exact field names: order_id, order_date, sentiment, reported_issues.
No markdown blocks, no explanation after the JSON.

Customer Feedback: "{feedback}"
```

**System Message:** `"You are a data extraction engine. Think step by step then output clean JSON only. No markdown. Use snake_case field names exactly as specified."`

**Why it works:**
- Step-by-step reasoning catches edge cases before committing to output
- Explicit field names in snake_case prevent `"Order ID"` vs `"order_id"` inconsistency
- `rfind('{')` and `rfind('}')` extract the final JSON block from the CoT response
- `max_tokens=300` gives enough room for reasoning text plus final JSON

---

## 4. Techniques — What Worked Best Per Task

| Technique | Best For | Why |
|-----------|----------|-----|
| Role alignment | All tasks | Fixes identity vs task conflict immediately |
| max_tokens | Classification | Hard enforcement that prompts alone can't provide |
| Few-shot examples | Classification + Generation | Shows exact format — eliminates ambiguity |
| Chain-of-Thought | Extraction | Forces reasoning through edge cases before output |
| Structured instructions | All tasks | Tells model what to do — good baseline before examples |

---

## 5. Reflection

### What failure patterns did I identify?

The most consistent failure pattern across all three tasks was **role-task conflict** — the default system message `"You are a helpful assistant"` actively worked against every task. Sentiment analysis needed a classifier, product description needed a copywriter, extraction needed a parsing engine. None of those roles are "helpful assistant." The model resolved the conflict by being helpful in the wrong direction every time.

A second pattern was **format ambiguity** — v1 prompts told the model what to do but never what the output should look like. The model filled that gap with its own preferences: conversational prose for sentiment, invented product names and variable length for descriptions, markdown-wrapped JSON for extraction. Every failure was the model making a reasonable decision with insufficient guidance.

The most surprising finding was that **binary pass/fail hid real failures entirely** for product description. A 100% success rate at a low bar made v1 look fine. Only when I tracked word count and standard deviation did the real problems — 292 average words, 15 unique product names — become visible.

### Which techniques had the biggest impact?

Role alignment in the system message had the single biggest immediate impact across all three tasks. It was a one-line change that fixed the fundamental mismatch between identity and task before any prompt rewriting was needed.

Few-shot examples had the biggest impact on consistency. For sentiment analysis, unique responses dropped from 15 out of 15 in v1 to 1 out of 15 in v3. The examples didn't just improve accuracy — they made the model's behaviour predictable and repeatable, which is what production systems actually need.

### What would I do differently next time?

I would fix the system message first before rewriting any prompt. Role alignment is the highest leverage change and it costs nothing — yet it was consistently the most impactful single improvement. Starting there would have reached good results faster.

I would also define success metrics before running any tests. Having word count targets and consistency thresholds set upfront would have surfaced the real product description failures in the first 5-run test instead of discovering them in the 15-run analysis. Measuring the right things from the start makes iteration faster and more purposeful.

---

## 6. Time Log

| Stage | Description |
|-------|-------------|
| Part 1 | Initial prompts and baseline testing |
| Part 2 | 5, 10, 15 run systematic testing |
| Part 3 | v2 structured prompt rewrites |
| Part 4 | v3 few-shot and CoT implementation |
| Part 5 | Task variations and final evaluation |

*Note: Exact timestamps recorded in Cell 26 of the notebook via `LAB_START` and `LAB_END` variables.*

---

## 7. Files Submitted

| File | Description |
|------|-------------|
| `prompt_engineering_lab_Pedro_Biain.ipynb` | Main notebook with all code and outputs |
| `failure_analysis.json` | Raw failure data from 15-run extraction test |
| `failure_analysis_table.csv` | Failure data in tabular format |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore rules |
| `lab_report.md` | This document |
