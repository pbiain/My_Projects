# Lab: Evaluation Score Distribution Dashboard
**Student:** Pedro Biain
**Tool used:** Tableau Desktop 2026.1
**Week 7 — Data Visualization & Reporting Tools**

---

## Dashboard Overview

This dashboard visualizes salary distribution across 15,000 AI job postings, built as a stakeholder-facing communication layer that answers three key business questions:

1. **What does the AI salary landscape look like overall?** → Salary distribution histogram
2. **How does seniority affect compensation?** → Average salary by experience level
3. **Does remote work come with a salary tradeoff?** → Salary by remote work type

---

## Data Source

AI Jobs Market dataset (15,000 rows, 19 columns). Fields used: `salary_usd` as the numeric metric, `experience_level` and `remote_ratio` as the primary analytical categories. See `data_source.md` for full mapping to lab requirements.

---

## Visualizations Built

| Sheet | Chart Type | Key Insight |
|---|---|---|
| Salary Distribution | Histogram (bins = $10K) | Most AI jobs pay $60K–$100K, right-skewed tail |
| Average Salary by Experience Level | Bar chart | Clear salary progression: Entry → Mid → Senior → Executive |
| Salaries by Remote Type | Grouped bar chart | No salary difference between Remote, Hybrid, and On-site |

---

## Communication Layer Principles Applied

- No p-values, confidence intervals, or statistical methodology shown
- All chart titles are written in plain business language
- Dashboard answers "what" and "so what" — not "how"
- Interactive filters allow stakeholders to explore without needing technical knowledge
- Color used to encode experience level category, not decoration

---

## Files

- `evaluation_score_dashboard.twbx` — Tableau packaged workbook
- `dashboard_screenshot.png` — Final dashboard screenshot
- `data_source.md` — Data source documentation
- `README.md` — This file
