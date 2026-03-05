# Self-Evaluation — Autonomous Real Estate Sales Funnel Agent
**IronHack AI Bootcamp · Module 3 · Solo Project · 5-Day Build**

---

## Scores (self-assessed)

| Outcome | Score | Notes |
|---|---|---|
| 1. Technical requirements | 2 | All core components implemented and deployed in production |
| 2. Agent architecture (ReAct + LangGraph) | 2 | Dual ReAct implementation + refactored async LangGraph pipeline |
| 3. RAG + API tools | 1.5 | RAG solid, tools work, MCP via @tool decorator |
| 4. N8N integration | 1.5 | N8N as logging/notification layer; Python handles orchestration |
| 5. Report quality + documentation | 1.5 | Live Google Sheets report, README, session logs, this file |

**Total: ~8.5 / 10**

---

## Self-Reflection

### What do you like most about your project?

On a technical level: the dual-mode architecture — an inbound AI sales agent that qualifies leads in real-time, combined with an outbound prospecting engine for finding real estate agencies and investors. It feels like a complete product, not a school exercise.

On an emotional level: the satisfaction of seeing my parents use this agent. My mother sends me feedback to improve the responses. That feeling of building something real for people you care about is different from passing a test. And seeing the Google Sheets auto-populate with classified leads after a conversation — that felt almost magical.

---

### What would you change if you started from scratch?

I wouldn't trade the learning curve or the mistakes — they were necessary. But knowing what I know now, I would invest more time upfront in structural design and write pseudocode that's Python-first from day one. N8N would be my operational complement, not the backbone I tried to build everything around.

Many N8N workflows I designed during the first days never made it to the final project. That time could have been spent in Python. The refactoring I had to do on my LangGraph architecture — particularly around the sequential blocking pipeline — could have been avoided with an async-first design from the beginning.

---

### What would you like to add when you have more time?

Front-end improvements — mobile responsiveness works but wasn't designed that way from the start. On the research side, I'd experiment with more APIs and spend more time on prompting so the logged contacts are more relevant and actionable. Longer term: a landing page, an ads strategy connected to the chatbot, a real-time voice bot, and a simplified lot map so clients can visually see what they are looking at. A form linked to the CTA button so leads can submit their contact details directly.

---

### What was the biggest challenge you faced, and how did you overcome it?

Three challenges stand out:

1. **Business logic** — understanding what kind of prospects to search for and how to find them online. Buyers don't post publicly; agencies and investment groups do. Took longer than expected to figure this out and adapt the search queries accordingly.

2. **The N8N pivot** — realizing on Day 1-2 that the N8N-first architecture I planned wasn't going to work for a Python-heavy project. Having to rebuild my mental model mid-project was disorienting but instructive. I learned the hard limits of visual workflow tools when you need loops and complex state.

3. **Response latency** — the agent ran 6 sequential nodes including two LLM calls before returning anything to the user. I solved it by decoupling the user-facing pipeline (retrieve → react → assemble) from classification and notifications, running the latter asynchronously in background threads. Response time roughly halved.

---

### How did you implement the ReAct pattern, and what did you learn about agentic AI?

The ReAct pattern appears in two forms in this project.

For the **outbound engine**: `create_react_agent` with two tools — `prospect_search` (Tavily web search) and `hunter_email_search` (Hunter.io). Here the user explicitly triggers tool use via UI buttons — the agent responds to user intent rather than calling tools autonomously.

For the **inbound chatbot**: the ReAct structure is implicit in the LangGraph graph itself. Each message triggers a loop — retrieve context (observe), reason with the LLM (think), classify and notify (act). The graph IS the reasoning loop; the notification channels are the actions.

The main thing I learned: agentic AI isn't just about making the LLM smarter — it's about designing the workflow around it so it can act on what it knows.

---

### What was your experience with LangGraph? How did you design your workflow?

LangGraph's `StateGraph` was the backbone of the project. State is just a dictionary that flows between node functions — once I understood that, adding or removing steps became clean and predictable.

I started with 6 nodes running sequentially, then refactored to 3 user-facing nodes (retrieve → react → assemble) with classification and notifications running asynchronously in background threads. The key insight: separate what the user waits for from what can happen silently in the background.

---

### How did you integrate the MCP tools, and what challenges did you face?

Tools are integrated via LangChain's `@tool` decorator — the LangChain implementation of the same standardized tool-calling protocol that MCP formalizes. Both approaches solve the same problem: exposing documented, structured capabilities to an LLM so it can reason about when and how to call them.

Two tools implemented:
- `prospect_search` — Tavily web search API for finding real estate agencies and investors
- `hunter_email_search` — Hunter.io API for email and phone discovery by domain

In this project, the user explicitly triggers the tools via the UI — a deliberate design decision to keep the human in the loop on outbound prospecting.

---

### What did you learn about deploying AI agents in N8N using Python runner or custom nodes?

N8N works best as a lightweight notification and logging layer, not as the orchestration backbone for a Python-heavy agent. The agent POSTs structured JSON to an N8N webhook; N8N routes it to Google Sheets for all sessions and could route Telegram/Gmail at scale.

The biggest lesson: N8N's visual workflows are powerful for simple routing but become unwieldy when you need loops, complex state, or conditional logic that LangGraph handles naturally in Python. I ended up inverting the original architecture — instead of N8N calling Python, Python calls N8N. Much cleaner.

---

### How did your RAG system perform? What would you improve?

Works well for property-specific questions using Pinecone with `text-embedding-3-large` (1024 dimensions). The main challenge wasn't the retrieval system itself — it was data quality. The source documents had conflicting prices (two different proposals with different per-m² rates). I resolved this by:

- Cleaning the Pinecone index (deleted conflicting PDFs, re-ingested 2 clean documents, 69 chunks)
- Hardcoding the verified prices in the system prompt as ground truth that overrides any RAG output
- Tightening the system prompt with few-shot examples and explicit rules

A reranker would be overkill for this volume of documentation and would slow response times significantly. Semantic chunking would have been interesting but unnecessary — cleaning the data and optimizing the prompt gave better results.

---

### If you were to build this for a real client, what would you do differently?

It already is deployed for real clients — my parents, who are selling lots at Amarras San Pedro. My mother gives regular feedback on the agent's responses. Next steps:

- Buy a domain and embed the chatbot into their actual website
- Build a native mobile app wrapper from the Railway URL
- Add a form to the CTA button so leads can submit contact details directly
- Improve outbound research quality with better query engineering and more API sources
- Proper mobile-first responsive redesign
- Continue refining the agent prompting, especially around payment plans and lot availability
- Add a CRM-style lead history dashboard over time
