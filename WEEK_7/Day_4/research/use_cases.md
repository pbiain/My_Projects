# Use Case Proposals: AI for Regional Haulage SME
**Project 5 — SilverTrust AI Consulting Simulation**  
**Prepared by:** Pedro  
**Date:** March 2026  
**Client:** Chleo — Regional Haulage SME, 50–200 employees, B2B, Spain  

---

## Context

Chleo's company operates a regional haulage fleet in Spain. Her primary concern is that AI is not transparent. Her primary business pain is fuel costs eating into margins. The use cases below are selected specifically for a company of this size and sector — practical, explainable, and delivering measurable ROI within 12 months.

Three use cases are proposed, ordered by priority and time to value.

---

## Use Case 1 — Fuel Cost Intelligence Dashboard

### What it is
A real-time monitoring system that tracks fuel consumption per truck, per driver, and per route — and flags anomalies automatically when consumption exceeds expected thresholds.

### Business problem it solves
Chleo currently has no visibility into *why* her fuel bill is what it is. She knows the total at the end of the month but cannot attribute it to specific trucks, drivers, or routes. This makes it impossible to act on.

### How it works
1. Trip and cost data is ingested from the TMS and fuel card system (or in this project, from `fFreight.csv` and `fCosts.xlsx`)
2. A baseline fuel consumption model is built per truck type and route distance
3. Any trip that deviates more than X% from baseline triggers an alert
4. A PowerBI dashboard surfaces the top fuel-consuming trucks, drivers, and routes weekly
5. An AI agent generates natural language insights: *"Truck 12 consumed 18% more fuel than average on the Barcelona–Valencia corridor last week. Likely causes: load weight above threshold or driver idle time."*

### Why it fits an SME of this size
- Uses data Chleo already has (fuel cards, TMS)
- No complex infrastructure required — runs on cloud APIs
- Dashboard is self-explanatory for a non-technical CEO
- Full transparency: every alert shows the data behind it (addresses Chleo's concern directly)

### Tools
- **Data:** `fFreight.csv` + `fCosts.xlsx` + `DimensionTables.xlsx`
- **Dashboard:** PowerBI
- **Monitoring:** LangSmith (tracks every AI insight generated)
- **Automation:** n8n (triggers alerts when anomaly detected)
- **LLM:** GPT-4o-mini or Claude Sonnet for insight generation

### KPIs
| Metric | Baseline | Target (6 months) |
|---|---|---|
| Fuel cost per km | Current average | -5% |
| % trips with anomaly detected | 0% (no visibility) | 100% monitored |
| Time to detect fuel anomaly | End of month | Same day |

### Estimated cost
- Setup: €8,000–12,000 (data pipeline + dashboard + agent)
- Monthly running: €200–400 (API costs + hosting)
- **Payback period: 2–3 months** at 5% fuel saving on a 50-truck fleet

---

## Use Case 2 — Automated Operations Alerts (n8n Workflow)

### What it is
An automation layer that replaces manual dispatch calls, WhatsApp messages, and Excel updates with triggered, real-time notifications to the right person at the right time.

### Business problem it solves
Operations managers in SME haulage companies spend significant time chasing status updates — calling drivers, updating spreadsheets, notifying clients of delays. This is low-value work that AI can automate entirely.

### How it works
1. Trip data is monitored in real time against planned ETAs
2. When a delay is detected (actual ETA > planned ETA by threshold), n8n triggers automatically:
   - Operations manager receives a Telegram/email alert with trip details
   - Client receives an automated delay notification
   - Delay is logged to Google Sheets for weekly reporting
3. When a fuel anomaly is detected (from Use Case 1), n8n triggers:
   - Fleet manager receives an alert with truck ID, route, and % deviation
4. End of day: n8n sends a summary report to management automatically

### Why it fits an SME of this size
- Replaces manual processes with zero new software purchases
- n8n runs on cloud — no IT infrastructure needed
- Highly visible impact from day one — Chleo sees automation working immediately
- Easy to demonstrate in a meeting as a live proof of concept

### Tools
- **Automation:** n8n (cloud)
- **Triggers:** Fuel anomaly detection, delay detection
- **Outputs:** Telegram alerts, Gmail notifications, Google Sheets logging
- **Data source:** `fFreight.csv` + `fCosts.xlsx`

### KPIs
| Metric | Baseline | Target |
|---|---|---|
| Time to notify client of delay | 30–60 min (manual) | Under 5 min (automated) |
| Daily reporting time | 45 min manual | 0 min (automated) |
| Fuel anomaly response time | End of month | Same day |

### Estimated cost
- Setup: €2,000–4,000 (workflow design + testing)
- Monthly running: €50–100 (n8n cloud subscription)
- **Payback period: Immediate** — operational efficiency from week one

---

## Use Case 3 — AI Insight Generator with LangSmith Monitoring

### What it is
An AI agent that analyses the fleet's operational and cost data weekly and produces a set of prioritised, explainable business insights — with full monitoring via LangSmith to demonstrate transparency.

### Business problem it solves
Chleo fears AI is a black box. This use case directly addresses that fear by showing her not just what the AI recommends, but exactly what data it used, what reasoning it applied, and how confident it is. LangSmith makes every AI decision auditable.

### How it works
1. Every week, the agent ingests the latest trip and cost data
2. It runs analysis across five dimensions: fuel efficiency, route performance, driver behaviour, cost trends, and anomalies
3. It generates 5–10 natural language insights ranked by business impact
4. Every insight is logged in LangSmith with: input data, prompt used, model response, latency, and cost
5. Chleo can open LangSmith and see exactly what the AI was asked, what it saw, and what it said

### Example insights generated
- *"Driver 7 has the highest fuel efficiency in the fleet this month — 12% below average consumption. Recommend sharing their driving pattern data with the rest of the team."*
- *"Route Madrid–Bilbao is generating 23% lower net revenue per km than the fleet average. Review pricing or load optimisation on this corridor."*
- *"Truck 23 has missed its scheduled maintenance window by 14 days. Based on current mileage, risk of unplanned breakdown is elevated."*

### Why it fits an SME of this size
- Directly addresses Chleo's transparency concern — she can see every decision the AI makes
- Insights are in plain Spanish business language, not technical jargon
- LangSmith monitoring doubles as a compliance and audit trail
- Scales easily — same agent works for 50 trucks or 200 trucks

### Tools
- **Agent framework:** LangChain / LangGraph
- **LLM:** GPT-4o-mini or Claude Sonnet
- **Monitoring:** LangSmith (full observability)
- **Data:** `fFreight.csv` + `fCosts.xlsx` + `DimensionTables.xlsx`
- **Dataset:** Small curated evaluation dataset created in LangSmith

### KPIs
| Metric | Baseline | Target |
|---|---|---|
| AI insights generated per week | 0 (no AI) | 5–10 actionable insights |
| Insight accuracy (human validated) | — | >80% rated useful by ops team |
| AI decision transparency | 0% (black box) | 100% (every decision logged) |
| LangSmith monitoring coverage | — | 100% of agent runs tracked |

### Estimated cost
- Setup: €6,000–10,000 (agent development + LangSmith integration)
- Monthly running: €150–300 (LLM API + LangSmith)
- **Payback period: 3–4 months** based on insight-driven fuel and route savings

---

## 4. Use Case Summary

| | UC1: Fuel Dashboard | UC2: Ops Alerts | UC3: AI Insights |
|---|---|---|---|
| **Priority** | 1 | 2 | 3 |
| **Time to value** | 3–6 months | 1–2 months | 4–6 months |
| **Setup cost** | €8–12k | €2–4k | €6–10k |
| **Monthly cost** | €200–400 | €50–100 | €150–300 |
| **Primary tool** | PowerBI + n8n | n8n | LangSmith + LangChain |
| **Addresses transparency** | Yes | Partially | Directly |
| **Complexity** | Medium | Low | Medium |

**Total estimated setup cost: €16,000–26,000**  
**Total estimated monthly running cost: €400–800**  
**Combined annual saving potential: €80,000–150,000** (fuel optimisation + empty km reduction + operational efficiency)

---

## 5. Why These Three Use Cases for This Company Size

A 50–200 employee haulage company has specific constraints that shaped these choices:

- **No in-house data team** — all tools must be manageable by a non-technical ops manager
- **Thin margins** — payback must be under 6 months to get board approval
- **Sceptical CEO** — transparency and explainability are non-negotiable
- **Existing data** — all three use cases work with data Chleo already produces, no new data collection required
- **Scalable** — all three use cases scale linearly as the fleet grows from 50 to 200 trucks
