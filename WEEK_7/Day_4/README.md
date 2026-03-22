# Fleet Cost Intelligence Dashboard
### Project 5 — SilverTrust AI Consulting Simulation
**IronHack AI Bootcamp | Week 7 | Pedro Biain**

---

## Overview

This project simulates a real AI consulting engagement for Chleo, the CEO of a regional haulage SME (50–200 employees) operating in Spain. Chleo's primary concern was that AI is not transparent. Her primary business pain is fuel costs eating into margins.

The deliverable is a complete AI consulting package: sector research, BI dashboard, automated n8n workflow, LangSmith monitoring, AI insight agent, and cost/timeline estimation.

**Sector:** Road freight / regional haulage  
**Company size:** SME (50–200 employees)  
**Pain point:** Fuel costs (30–35% of operating costs)  
**AI hook:** Fuel anomaly detection with full transparency via LangSmith  

---

## Project Structure

```
Day_4/
├── agent/
│   ├── agent.py
│   ├── tools.py
│   └── insights_generator.py
├── cost_estimation/
│   ├── cost_analysis.md
│   ├── timeline_estimate.md
│   └── images/
├── dashboard/
│   └── chleo_cost_intelligence_dashboard.twbx
├── data/
│   ├── raw/
│   └── processed/
│       ├── processed_costs.csv
│       ├── processed_freight.csv
│       ├── dim_drivers.csv
│       ├── dim_vehicles.csv
│       └── dim_customers.csv
├── langsmith/
│   ├── dataset_creation.py
│   ├── monitoring_setup.py
│   └── monitoring_results/
│       ├── experiment_summary.png
│       └── example_detail.png
├── n8n/
│   ├── workflow.json
│   └── workflow_documentation.md
├── research/
│   ├── sector_research.md
│   ├── opportunities_risks.md
│   └── use_cases.md
├── .env.example
├── .gitignore
├── evaluation_report.md
├── requirements.txt
└── README.md
```

---

## Use Cases

Three AI use cases proposed for Chleo's fleet:

**UC1 — Fuel Cost Intelligence Dashboard**
Real-time monitoring of fuel consumption per truck, per driver, per month. Anomaly detection flags trucks burning 20%+ above fleet average. Built in Tableau with data from synthetic TMS + fuel card datasets.

**UC2 — Automated Operations Alerts (n8n)**
Daily automated workflow: reads fleet cost data → detects anomalies → sends Gmail alerts → logs to Google Sheets and Airtable. Replaces manual dispatch calls and end-of-month reporting.

**UC3 — AI Insight Generator with LangSmith Monitoring**
LangChain agent generates weekly natural language insights from fleet data. Every AI decision is logged in LangSmith — what data went in, what the model said, and why. Directly addresses Chleo's concern about AI transparency.

---

## Dataset

**Source:** Synthetic freight datasets (Kaggle)  
**Files used:**
- `fFreight.csv` — 92,060 trip records (Jan 2018 – Aug 2019)
- `fCosts.xlsx` — 295 monthly cost records per truck
- `DimensionTables.xlsx` — Drivers, Vehicles, Customers lookup tables

**Note:** Customer locations are US-based (synthetic). In a real engagement, data would be extracted from the client's telematics platform (Webfleet, Samsara) and fuel card provider (DKV, UTA).

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/pbiain/My_Projects
cd WEEK_7/Day_4
```

### 2. Create and activate environment
```bash
conda activate ironhack_env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

Required keys:
```
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=chleo-fuel-intelligence
LANGCHAIN_TRACING_V2=true
```

---

## How to Run

### Create LangSmith dataset
```bash
python langsmith/dataset_creation.py
```
Generates 10 AI insights from fleet data and uploads them to LangSmith.

### Run LangSmith experiment
```bash
python langsmith/monitoring_setup.py
```
Runs the evaluation experiment with 3 custom evaluators (relevance, actionability, clarity). Results visible at [smith.langchain.com](https://smith.langchain.com).

### View the dashboard
Open `dashboard/chleo_cost_intelligence_dashboard.twbx` in Tableau Desktop.

### Run the n8n workflow
Import `n8n/workflow.json` into your n8n instance. Configure Gmail and Google Sheets credentials. Activate the workflow.

---

## LangSmith Links

- **Dataset:** [chleo-fuel-intelligence-insights](https://smith.langchain.com/o/aad83da9-5bc6-4913-8dfb-ab739f390dcc/datasets/6de796a4-c1e5-429c-81f0-2387d1610947)
- **Experiment:** [fuel-insight-evaluation-658a3078](https://smith.langchain.com/o/aad83da9-5bc6-4913-8dfb-ab739f390dcc/datasets/6de796a4-c1e5-429c-81f0-2387d1610947/compare?selectedSessions=09bf8605-671b-4b2a-892c-fe4164e42de2)

**Experiment results:** 0.94 average insight quality, 1.00 actionability, 2.30s P50 latency across 10 examples.

---

## Key Results

| Metric | Value |
|---|---|
| Total fleet fuel spend (dataset) | €901,895 |
| Top fuel consumer | Truck 17 (~€132,736) |
| Anomalies detected by n8n | 93 trips above 20% threshold |
| LangSmith insight quality score | 0.94 / 1.00 |
| Estimated year 1 ROI | 178% |
| Estimated payback period | 4.3 months |

---

## Research Documents

- [Sector Research](research/sector_research.md) — European road freight market analysis
- [Opportunities & Risks](research/opportunities_risks.md) — AI opportunity mapping for logistics SME
- [Use Cases](research/use_cases.md) — Three proposed AI use cases with KPIs and cost estimates
- [Cost Analysis](cost_estimation/cost_analysis.md) — Full cost breakdown and ROI calculation
- [Timeline](cost_estimation/timeline_estimate.md) — 24-week phased implementation plan
- [Evaluation Report](evaluation_report.md) — LLM-as-judge evaluation with bias discussion

---

## .env.example

```
OPENAI_API_KEY=your_openai_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=chleo-fuel-intelligence
LANGCHAIN_TRACING_V2=true
```

---

## Requirements

See `requirements.txt` for full list. Key dependencies:
```
langsmith
langchain
openai
pandas
python-dotenv
```
