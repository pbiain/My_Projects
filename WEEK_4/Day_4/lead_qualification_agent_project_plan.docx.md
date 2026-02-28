**AUTONOMOUS AGENT PROJECT PLAN**

*Lead Qualification Agent*

Week 4 — Day 4  |  AI Consultant Project

# **1\. Use Case**

## **Problem Statement**

Sales teams at small-to-medium businesses waste valuable time manually reviewing every lead that comes in through web forms or email. A person has to read the submission, decide if it is worth pursuing, sometimes send follow-up questions, wait for a reply, and then decide whether to route the lead to a salesperson. This process is slow, inconsistent, and prone to human error — good leads go cold while the team is busy, and bad leads eat up time that should be spent closing deals.

An autonomous Lead Qualification Agent solves this by handling the entire triage process automatically: receiving the lead, asking intelligent follow-up questions, scoring the lead against a qualification rubric, and routing it to the right person — all within minutes, not hours.

## **Target Users**

* Sales representatives at SMBs who receive high volumes of inbound leads

* Sales managers who need consistent qualification criteria applied at scale

* Marketing teams that run campaigns and need to filter responses automatically

## **Success Criteria**

* Agent correctly qualifies or disqualifies at least 80% of leads without human intervention

* Lead routing happens within 2 minutes of form submission

* Sales team reports reduction in time spent on manual lead triage

* No qualified leads fall through the cracks (zero missed hot leads)

## **Current Manual Process**

Today, a human reads each incoming lead form, optionally sends a follow-up email with clarifying questions, waits 1–48 hours for a reply, makes a subjective judgment on fit, and then forwards the lead to the appropriate salesperson. This takes between 30 minutes and 2 days per lead depending on response times, and quality is inconsistent across different team members.

# **2\. Technology Stack**

## **Selected Technologies**

| Component | Technology | Why This Choice |
| :---- | :---- | :---- |
| Core LLM | OpenAI GPT-4o | Best reasoning for nuanced qualification decisions; strong instruction-following |
| Vector Database | ChromaDB (local) or Pinecone (cloud) | Stores ideal customer profile docs for RAG; fast semantic search |
| Embeddings | OpenAI text-embedding-ada-002 | High quality, cost-effective, integrates natively with LangChain |
| Agent Framework | LangGraph | Multi-step workflow: receive → ask → score → decide → route |
| Orchestration | n8n | Triggers on new form submissions; connects email, CRM, and Slack |
| Tools / Integrations | Gmail API, Slack API, Airtable/Not-HubSpot too complex | Email follow-up, team notifications, lead logging |

## **Why LangGraph Over Simple LangChain?**

Think of LangGraph like a flowchart with memory. A simple LangChain agent is like a chef who improvises every dish. LangGraph is like a chef with a written recipe — each step is defined, decisions are structured, and the process is repeatable. Our qualification flow has clear stages (receive → question → score → route), which maps perfectly to LangGraph's state machine model.

## **Why n8n for Orchestration?**

n8n acts as the 'central nervous system' connecting all the external tools. Instead of writing custom integration code for every service (Gmail, Slack, HubSpot), n8n provides visual workflows with pre-built connectors. It listens for new leads 24/7 and triggers the agent automatically — no human needs to press a button.

## **Alternatives Considered**

* AutoGen: Powerful for multi-agent conversations but overkill for a linear qualification flow

* Simple LangChain ReAct agent: Faster to build but lacks the structured state management we need

* Zapier instead of n8n: Easier UI but limited flexibility and higher cost at scale

# **3\. MVP Scope**

## **What Is Included in MVP**

| Feature | Priority | Description |
| :---- | :---- | :---- |
| Receive lead from web form | Must-have | n8n watches for new form submissions (Google Forms or Typeform) |
| Send follow-up questions via email | Must-have | Agent sends 2–3 clarifying questions to the lead automatically |
| Score lead as Qualified / Unqualified | Must-have | LangGraph scores against ideal customer profile stored in RAG |
| Notify sales team on Slack | Must-have | Qualified leads trigger a Slack message with lead summary |
| Log all leads to Airtable | Must-have | Every lead and its outcome is recorded for review |
| Conversation memory per lead | Must-have | Agent remembers the follow-up Q\&A thread for context |

## **What Is Excluded from MVP (Future Versions)**

* CRM deep integration (Salesforce, HubSpot workflows) — v2

* Multi-language support — v2

* Voice or chatbot interface — v2

* Automated phone call via Twilio — v3

* Google Calendar scheduling for sales calls — v3

* Advanced lead scoring with weighted criteria and ML — v3

* Analytics dashboard — v3

* Mobile app — v3+

## **MVP Success Metrics**

* 80%+ qualification accuracy vs human benchmark on test set of 20 leads

* Average response time under 2 minutes from form submission to Slack notification

* Zero qualified leads lost or unnoticed in a 2-week pilot

* Sales team spends 50% less time on manual lead review

# **4\. Risk Assessment**

| Risk | Probability | Impact | Mitigation Strategy |
| :---- | :---- | :---- | :---- |
| LLM hallucinates qualification (false positives/negatives) | Medium | High | Add human review step for borderline scores; set confidence threshold below which agent flags for human |
| High API costs from excessive LLM calls | Medium | High | Cache common queries; use GPT-3.5 for simple tasks; set cost alerts; optimize prompts to reduce tokens |
| Lead does not reply to follow-up questions | High | Medium | Set 48-hour timeout; auto-disqualify silent leads; flag for optional human follow-up |
| Email integration breaks or lands in spam | Low | High | Monitor email delivery rates; use SendGrid as backup; log all outbound emails |
| CRM/Airtable integration fails | Low | Medium | Write to local CSV as fallback; send admin alert; retry logic in n8n |
| Scope creep: team asks for more features mid-build | High | Medium | Lock MVP features in writing before build; use backlog for v2 requests |
| Privacy / GDPR concern with storing lead data | Medium | High | Only store necessary fields; define data retention policy; encrypt personal identifiable information (PII) at rest (somewhere, like pinecone or airtable) |
| Ideal customer profile rubric is inaccurate | Medium | High | Validate rubric with sales team before building; run A/B test with human scorer in parallel |

# **5\. Implementation Plan**

## **Phase 1 — Setup & Data Preparation (Week 1\)**

* Set up development environment: Python, LangChain, LangGraph, n8n

* Create vector database (ChromaDB) and load ideal customer profile documents

* Test basic RAG: can the agent answer 'is this lead a good fit?' using the docs?

* Set up API keys: OpenAI, Gmail, Slack, Airtable

* Milestone: RAG returns accurate answers about customer fit criteria

## **Phase 2 — Core Agent Development (Week 2\)**

* Build LangGraph state machine: 5 nodes (receive → question → wait → score → route)

* Implement conversation memory so agent tracks follow-up replies

* Write qualification scoring logic with confidence thresholds

* Unit test agent with 10 sample leads (5 qualified, 5 not)

* Milestone: Agent correctly qualifies/disqualifies 8/10 test leads

## **Phase 3 — Integrations & Orchestration (Week 3\)**

* Build n8n workflow: trigger on Google Form submission → call agent → act on result

* Connect Gmail API for automated follow-up email sending

* Connect Slack API for qualified lead notifications

* Connect Airtable for lead logging

* End-to-end test: submit a form, agent qualifies, Slack notified, Airtable updated

* Milestone: Full pipeline runs without manual intervention

## **Phase 4 — Testing, Deployment & Monitoring (Week 4\)**

* Run 2-week pilot with real inbound leads alongside human reviewer

* Compare agent decisions vs human decisions; calculate accuracy

* Set up cost monitoring dashboard (OpenAI token usage alerts)

* Deploy to production environment (n8n cloud or self-hosted)

* Document runbook: how to update the rubric, how to handle errors

* Milestone: Agent live in production; sales team onboarded

| Phase | Duration | Key Milestone | Dependencies |
| :---- | :---- | :---- | :---- |
| 1 — Setup & Data | 1 week | RAG answering fit questions accurately | API keys, customer profile docs |
| 2 — Core Agent | 1 week | Agent qualifies 8/10 test leads correctly | Phase 1 complete |
| 3 — Integrations | 1 week | Full pipeline runs end-to-end | Phase 2 complete, API access |
| 4 — Deploy & Monitor | 1 week | Live in production with monitoring | Phase 3 complete, sales team buy-in |

# **6\. Success Metrics**

## **Quantitative Metrics**

* Qualification accuracy: ≥ 80% match with human benchmark

* Response time: ≤ 2 minutes from form submission to Slack notification

* Cost per lead processed: ≤ $0.05 in API calls

* Lead loss rate: 0% qualified leads missed or dropped

* Time saved: ≥ 50% reduction in manual triage time for sales team

## **Qualitative Metrics**

* Sales team satisfaction: team reports qualification quality is consistent and reliable

* Adoption rate: team actively uses agent output rather than re-qualifying manually

* Trust: no incidents of 'I had to override the agent' in first month

## **How We Will Measure**

During the 2-week pilot (Phase 4), a human reviewer will independently score the same leads the agent processes. We will compare outcomes side-by-side and calculate precision and recall. Cost will be tracked via OpenAI's usage dashboard. Speed will be logged by n8n's execution timestamps. Sales team feedback will be collected via a weekly 5-question survey.

# **7\. Resources Needed**

| Resource | Details | Estimated Cost |
| :---- | :---- | :---- |
| OpenAI API | GPT-4o for reasoning, ada-002 for embeddings | \~$0/month (Ironhack API)|
| n8n | Self-hosted (free) or n8n Cloud Starter | $0–20/month |
| ChromaDB | Local vector store (free) or Pinecone Starter | $0/month |
| Airtable | Free tier for lead logging | $0/month |
| Gmail API | Free via Google Cloud Console | $0/month |
| Slack API | Free for basic notifications | $0/month |
| Developer time | 1 person, \~4 weeks part-time | Internal cost |

*Document prepared for Week 4 Day 4 — Autonomous Agent Challenge*