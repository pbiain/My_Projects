# VaultGuard Billing Validation AI — MVP

**Status: Live**

---

## Is this an MVP or a POC?

It's an MVP.

A POC proves something works on test data. An MVP works on real data and delivers real value to a real user.

This pipeline runs on a live Gmail inbox, processes real invoice batches, and delivers ready-to-use spreadsheets to the billing team. A person who used to spend hours reviewing invoices manually can now open their email and find the work already done.

That's an MVP.

---

## What it does

Every time a SafeCore invoice batch arrives by email:

1. The pipeline picks it up automatically
2. Reads every invoice out of the PDF (typically 40+ per email)
3. Classifies each one — should VaultGuard bill the client, or absorb the cost?
4. Emails the billing team two spreadsheets:
   - **Working sheet** — full detail with the AI's reasoning, for human review
   - **Oracle Upload sheet** — ready to paste into the billing system

No manual steps. One email in, two spreadsheets out, in under 5 minutes.

---

## What's still rough (v1.1 items)

Three things stop this from being a fully polished product:

**1. Large batch rate limiting**
When a batch has 100+ invoices, OpenAI occasionally drops some requests. A small delay between calls fixes this — it's a configuration change, not a rebuild.

**2. Oracle upload is still manual**
The spreadsheet is formatted correctly for the WebADI bulk loader, but a human still has to open it and run the upload. Automating this final step is the next milestone.

**3. No accuracy tracking**
There's no dashboard yet showing whether the AI's decisions are drifting over time. Running in parallel with the human biller for 30 days and logging the override rate would give a real accuracy baseline.

---

## How it's built

| Part | What it does | Where it runs |
|---|---|---|
| n8n workflow | Watches Gmail, orchestrates the pipeline | n8n Cloud |
| Python API | Extracts invoices from PDF, classifies each one | Railway (always on) |
| OpenAI GPT-4o | Reads image-based PDFs, makes YES/NO decisions | OpenAI API |

The Python API and n8n talk over standard HTTP — no proprietary connectors, no lock-in.

---

## Requirements

See `requirements.txt` in this folder for the full dependency list.

To run the Python API locally:

```bash
pip install -r requirements.txt
python -m src.api_server
```

The server starts on `http://localhost:8080`. Set your `OPENAI_API_KEY` in a `.env` file first.
