# VaultGuard Billing Validation AI — POC Documentation

**Project:** VaultGuard × SafeCore Maintenance Intelligence Platform
**Author:** Pedro Biain — IronHack AI Bootcamp, Week 9 Capstone
**Date:** April 2026
**Status:** POC Complete — Pipeline running end-to-end

---

## The problem

Every month VaultGuard receives a batch of maintenance invoices from SafeCore. A human biller reviews each one and decides:

> Should this be billed to the client, or absorbed by VaultGuard?

This takes hours of manual work. And it's error-prone — analysis of the 2025 dataset (3,848 invoices) found **456 discrepancies**: $98,843 in potential over-billing and $22,915 in under-billed revenue that was never recovered.

The POC proves an AI can do this automatically, at scale, in minutes.

---

## What was built

A fully automated pipeline that:

1. **Watches a Gmail inbox** for incoming SafeCore invoice emails
2. **Downloads the PDF attachment** (a batch file — typically 40+ invoices per email)
3. **Extracts every invoice** from the PDF using GPT-4o vision (the PDFs are image-based, not text)
4. **Classifies each invoice** — YES (bill client) or NO (VaultGuard absorbs) — with a reason and confidence score
5. **Generates two spreadsheets** and emails them to the billing team:
   - **Working sheet** — full detail with AI reasoning, for human review
   - **Oracle Upload sheet** — stripped down, ready to paste into the billing system

No manual steps. One email in, two spreadsheets out.

---

## Architecture

```
Gmail inbox
    │
    ▼
n8n (cloud workflow)
    │  watches for SafeCore emails, downloads PDF attachment
    │
    ▼
Python API (Railway)
    │  renders each PDF page as an image
    │  sends to GPT-4o vision → extracts all invoices
    │  redacts customer PII before classification (GDPR)
    │  sends each invoice to GPT-4o → YES/NO decision
    │
    ▼
n8n (cloud workflow)
    │  merges invoice data with AI classification
    │  builds Working sheet + Oracle Upload sheet (CSV)
    │
    ▼
Email to billing team
    (2 CSVs attached + summary + flagged items list)
```

The Python API runs on Railway (cloud hosting) so n8n can call it from anywhere. The two services talk over standard HTTP — no proprietary connectors needed.

---

## How the AI makes decisions

The AI is given the exact decision rules from the White Glove Service contract:

**Bill the client (YES)** when the issue is caused by:
- Physical damage — broken screen, bent components, liquid spillage
- Abuse, vandalism, or negligence
- Foreign objects jammed in the bill acceptor
- Infestation (insects, rodents)
- Burglary damage
- Customer refused access or cancelled after dispatch

**VaultGuard absorbs (NO)** when the issue is:
- Normal wear and tear — validator springs, component ageing
- Communications or modem failure
- Software, firmware, or network problems
- User programming errors
- No fault found on site
- Printer jams or paper issues
- Equipment resets

The AI also uses the labour charge as a signal — $186/$189 confirms Zone 1–3 OOS rate, $621/$630 confirms Zone 4. Both indicate the technician classified the visit as out-of-scope.

For every invoice the AI returns:

| Field | What it means |
|---|---|
| Decision | YES (bill client) or NO (absorb) |
| Confidence | HIGH, MEDIUM, or LOW |
| Reason | One sentence explaining the decision |
| Key signal | The specific word or phrase that drove the decision |
| Flag for review | True when the AI is uncertain — routes to human biller |

---

## GDPR approach

Customer names, addresses, and contact details in invoices are personal data under GDPR. Before any invoice data is sent to OpenAI for classification, the pipeline automatically:

- Replaces the customer name, address, and postcode with a **pseudonymous token** (e.g. `CLIENT-A3F7C219`)
- The token is generated consistently — the same customer always gets the same token, so audit trails remain intact
- Removes all embedded images from PDF pages (logos, stamps) before rendering

The only step where personal data crosses the system boundary is the initial PDF extraction — this is documented in the DPIA and accepted as necessary for the service to function.

---

## POC results

Run on a live batch of 42 invoices from a single SafeCore email:

- All 42 invoices successfully extracted from the PDF
- Each invoice classified with a decision, confidence score, and plain-English reason
- Two CSVs generated and emailed in under 4 minutes
- Flagged invoices (low confidence or missing data) correctly identified for human review
- GL codes automatically assigned: 440133 (absorb) / 440134 (bill client)

From the 2025 historical dataset validation:

| Metric | Value |
|---|---|
| Match rate with human biller | 84.3% |
| Discrepancies identified | 456 of 3,848 |
| Over-billing risk flagged | $98,843 |
| Under-billing recovered | $22,915 |

---

## What this POC does not yet do

- **Batch size**: Rate limits on OpenAI mean very large batches (100+ invoices) need a small delay between classifications. This is a configuration change, not a code change.
- **Oracle upload**: The CSV is formatted for WebADI but the upload step is still manual — a human opens the file and runs the bulk loader. Automating this is a Pilot phase item.
- **Historical data**: The 2024 invoices lack structured OOS categories, so accuracy on that cohort is lower. The model performs best on 2025-format invoices.
- **Accuracy tracking**: There is no dashboard yet tracking human override rate over time. This is planned for the Pilot phase.

---

## Next steps (Pilot phase)

1. Run the pipeline in parallel with the human biller for 30 days — measure real override rate
2. Add Microsoft Teams notifications (replaces Gmail alerts, fits within existing M365 licence)
3. Build an accuracy dashboard in Power BI — track weekly match rate and flag trends
4. Automate the Oracle WebADI upload step
5. Extend to cover 2024-format invoices once OOS category data is backfilled

---

*Built as part of IronHack AI Bootcamp Week 9 Capstone — VaultGuard × SafeCore Maintenance Intelligence Platform*
