# 🏡 Amarras San Pedro — Real Estate Sales Agent

> Autonomous AI agent that qualifies inbound real estate leads, answers buyer questions from property documents, and routes notifications — without human intervention.

**Author:** Pedro Biain | **IronHack AI Bootcamp** | **Week 5 — Module 3**
**Stack:** Python 3.12 · LangGraph · LangChain · Pinecone · Flask · Railway · n8n · OpenAI · DuckDuckGo · Hunter.io · Telegram · Gmail · Google Sheets

---

## 📌 Project Overview

Amarras San Pedro is a nautical residential club development in San Pedro, Buenos Aires, Argentina. **Boating I** offers waterfront lots ranging from 544m² to 1,188m², with direct river access, private docks, and navigable canals. Price: U$S 120/m².

This agent automates the sales funnel:
- A potential buyer sends a question (via n8n webhook)
- The agent retrieves accurate answers from real property documents using RAG
- It classifies the lead as **HOT**, **WARM**, or **COLD**
- **HOT leads** → instant Telegram alert to the owner
- **WARM leads** → formatted HTML email with agent response
- **All leads** → logged to Google Sheets with timestamp and reason
- The agent answers the buyer's question autonomously — no human required

---

## 🏗️ Architecture

```
n8n Webhook → HTTP Request → ngrok → Flask (server.py)
                                           ↓
                                    LangGraph Pipeline
                                           ↓
                              retrieve_context (Pinecone RAG)
                                           ↓
                              react_agent (gpt-4o-mini + DuckDuckGo + Hunter.io)
                                           ↓
                              classify_lead (HOT / WARM / COLD)
                                           ↓
                              send_telegram (HOT only) → Python
                                           ↓
                              send_gmail (WARM only) → Python
                                           ↓
                              assemble_output → JSON → n8n
                                           ↓
                              Google Sheets (ALL leads) → n8n
```

### Lead Routing Logic

| Lead Score | Telegram | Gmail | Google Sheets |
|------------|----------|-------|---------------|
| 🔥 HOT | ✅ | ❌ | ✅ |
| 🌡️ WARM | ❌ | ✅ | ✅ |
| 🧊 COLD | ❌ | ❌ | ✅ |

---

## 📁 Project Structure

```
WEEK_5/
├── apart_agent/
│   ├── __init__.py
│   ├── state.py                  # AgentState TypedDict
│   ├── graph.py                  # LangGraph pipeline builder
│   └── nodes/
│       ├── __init__.py
│       ├── retrieve_context.py   # Pinecone RAG retrieval
│       ├── react_agent.py        # ReAct agent (gpt-4o-mini + DuckDuckGo + Hunter.io)
│       ├── prospect_search_tool.py  # DuckDuckGo web search tool
│       ├── hunter_tool.py        # Hunter.io email finder tool
│       ├── classify_lead.py      # HOT/WARM/COLD classifier
│       ├── assemble_output.py    # JSON output builder
│       ├── send_telegram.py      # Telegram Bot API (HOT)
│       └── send_gmail.py         # Gmail SMTP (WARM)
├── agent.py                      # CLI entry point
├── server.py                     # Flask server (POST /agent)
├── apart_agent.ipynb             # Development notebook + test suite
├── requirements.txt
└── .env                          # API keys (never committed)
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/pbiain/My_Projects.git
cd My_Projects/WEEK_5
```

### 2. Create and activate conda environment

```bash
conda create -n ironhack_env python=3.12
conda activate ironhack_env
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in `WEEK_5/`:

```env
# OpenAI
OPENAI_API_KEY=your_key_here

# Pinecone
PINECONE_API_KEY=your_key_here

# Hunter.io
HUNTER_API_KEY=your_key_here

# Telegram
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Gmail
GMAIL_SENDER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
GMAIL_RECIPIENT=recipient@gmail.com
```

> ⚠️ Never commit `.env` to GitHub. It is already in `.gitignore`.

### 5. Run the Flask server

```bash
python server.py
```

Server starts on `http://localhost:5678`.

### 6. Start ngrok (for n8n cloud integration)

```bash
ngrok http 5678
```

Copy the `https://` forwarding URL — this is what n8n calls.

---

## 🚀 Running the Agent

### Option A — CLI (direct, no n8n)

```bash
python agent.py "Tengo un presupuesto de U$S 50.000. ¿Qué parcelas puedo comprar?"
```

### Option B — via n8n webhook (full pipeline)

With `server.py` and ngrok running, trigger n8n with:

```powershell
$body = '{"message": "I am interested in buying a lot, what is the price?"}'
Invoke-RestMethod -Uri "https://YOUR-N8N-WEBHOOK-URL/webhook/apart-agent" -Method POST -ContentType "application/json" -Body $body
```

---

## 🧠 Technical Implementation

### ReAct Pattern

The ReAct (Reasoning + Acting) pattern is implemented inside `react_agent.py` using LangChain's `create_react_agent`. The agent:

1. **Reasons** — reads the retrieved property context and the lead's question
2. **Acts** — decides whether to call DuckDuckGo (market research) or Hunter.io (email lookup)
3. **Observes** — incorporates tool results into its reasoning
4. **Answers** — produces a grounded final answer from real documents

### LangGraph State Machine

State flows linearly through 6 nodes:

```
retrieve_context → react_agent → classify_lead → send_telegram → send_gmail → assemble_output
```

Each node receives and returns the full `AgentState` TypedDict. Notification filtering is handled inside each node (not via conditional edges), making the graph simple and deterministic.

### RAG System

- **Vector database:** Pinecone (`n8n` index, 69 vectors, `text-embedding-3-large`, 1024 dimensions)
- **Documents ingested (2 clean docs):**
  - `VALORES DE LOTES EN BOATING I.docx.pdf` — verified lot prices, parcel table, payment plans
  - `REGLAMENTO EDIFICACION-BOATING I.pdf` — building regulations, construction rules, lot restrictions
- **Retrieval:** Top-4 chunks filtered by cosine similarity score threshold (< 0.35 discarded), formatted as context string for the agent
- **Price authority:** Verified lot prices are hardcoded in the system prompt and override any RAG result — prevents pricing errors from conflicting documents

> **Note:** Two conflicting documents were removed from Pinecone (`Propuesta de inversión.pdf` contained wrong U$S 45/m² stage-2 pricing; a personal investment proposal PDF was not appropriate for a public chatbot). Pinecone was cleared and re-ingested from scratch with the 2 clean docs above.

### RAG Quality Improvements

Two techniques are implemented to prevent irrelevant retrieval, especially for short or vague follow-up messages.

#### 1. Query Contextualization (implemented — `retrieve_context.py`)

**Problem:** When a user sends a vague follow-up like *"how do I do that?"* or *"como hago eso?"*, the RAG query has no semantic content. Embedding a 4-word sentence retrieves random chunks (e.g., construction regulations) that have nothing to do with the conversation.

**Solution:** If the user message is ≤ 6 words and there is conversation history, the previous assistant reply is prepended to the RAG query before embedding:

```python
if len(words) <= 6 and state.get("chat_history"):
    last_turn = state["chat_history"][-1]
    rag_query = f"{last_turn['assistant']} {user_msg}"
else:
    rag_query = user_msg
```

**Why it works:** *"You can contact us directly at Amarras San Pedro! how do I do that?"* embeds to a vector that retrieves contact/sales chunks instead of construction rules. The RAG now understands the topic from context.

#### 2. Similarity Score Threshold (implemented — `retrieve_context.py`)

**Problem:** `similarity_search` always returns k results regardless of how relevant they are. A cosine similarity of 0.2 means the chunk is barely related — yet it gets passed to the agent as authoritative context.

**Solution:** `similarity_search_with_score` is used instead, and chunks below a cosine similarity threshold of 0.35 are discarded:

```python
results = vectorstore.similarity_search_with_score(rag_query, k=4)
for doc, score in results:
    if score < 0.35:
        continue          # discard low-relevance chunks
```

If all chunks are discarded, the agent falls back to conversation history and its hardcoded knowledge of Amarras San Pedro (prices, lots, amenities).

#### 3. Semantic Chunking (future improvement)

**Problem:** Fixed-size chunking (`RecursiveCharacterTextSplitter`, 800 chars) can split a pricing table mid-row or mix two unrelated topics in one chunk, reducing retrieval precision.

**Solution:** `SemanticChunker` (from `langchain_experimental`) uses the embedding model itself to detect topic boundaries. It splits where semantic similarity between consecutive sentences drops below a threshold — keeping each chunk topically coherent.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

splitter = SemanticChunker(OpenAIEmbeddings(model="text-embedding-3-large"))
chunks = splitter.split_documents(docs)
```

**Trade-off:** Requires re-ingesting Pinecone. Chunk count varies (can produce fewer, larger chunks). Adds cost since the splitter embeds every sentence to find boundaries. For a 2-document corpus, the quality gain is moderate — query contextualization + score filtering address the main issues first.

### Lead Classification

Zero-shot structured LLM call using `gpt-4o-mini` with `temperature=0`. Returns JSON `{score, reason}`.

Classification criteria:
- **HOT** — specific budget mentioned, asks about payment plans with intent to buy, mentions investment ROI, ready to proceed
- **WARM** — general interest, asking about prices or availability, building regulations, no urgency
- **COLD** — just browsing, vague, hypothetical, no real intent signals

---

## 🔌 API Integrations

| Tool | Integration | Purpose |
|------|-------------|---------|
| **OpenAI** | LangChain (`gpt-4o-mini`, `text-embedding-3-large`) | LLM reasoning + embeddings |
| **Pinecone** | `langchain_pinecone.PineconeVectorStore` | Vector search over property docs |
| **DuckDuckGo** | LangChain `DuckDuckGoSearchRun` tool | Real estate agency & lead prospect search |
| **Hunter.io** | `hunter_tool.py` via REST API | Email finder for outbound prospecting |
| **Telegram Bot API** | `requests` (direct HTTP) | HOT lead alerts to owner |
| **Gmail** | `smtplib` SMTP SSL | WARM lead HTML email notifications |
| **Google Sheets** | n8n `Append row in sheet` node | Full lead logging with timestamps |

---

## 🎨 Design Decisions

### Tool Integration Strategy

**LangChain tool interface (DuckDuckGo + Hunter.io)**
DuckDuckGo and Hunter.io are integrated via LangChain's `@tool` decorator, allowing the ReAct agent to autonomously decide when to search for real estate agencies or find professional email contacts.

**Direct Python integration (Telegram & Gmail)**  
Telegram and Gmail are implemented as deterministic LangGraph nodes rather than LLM-controlled tools. This was a deliberate architectural choice: notifications should always fire based on hard rules (HOT → Telegram, WARM → Gmail), not probabilistic LLM reasoning. Deterministic behavior is more reliable in a production notification system.

**n8n for orchestration, Python for logic**  
n8n handles the webhook entry point and Google Sheets logging. All business logic (RAG, classification, notifications) runs in Python. This separation makes the Python agent independently testable and keeps n8n as a thin orchestration layer.

### Flask + ngrok over n8n Execute Command

The n8n cloud version used in this project does not support the Execute Command node. Flask + ngrok was chosen as an equivalent solution: Flask exposes the agent as an HTTP endpoint, and ngrok creates a tunnel from n8n cloud to the local server.

---

## ⚠️ Known Limitations & Future Improvements

- **Semantic chunking:** Fixed-size chunking (800 chars) can split pricing tables mid-row. Replacing `RecursiveCharacterTextSplitter` with `SemanticChunker` would produce topic-coherent chunks and improve retrieval precision — see RAG Quality Improvements above.
- **Score threshold tuning:** The 0.35 cosine similarity cutoff was set conservatively. Logging retrieved scores in production would allow data-driven tuning.
- **Zero-shot classification:** The lead classifier uses zero-shot prompting. Few-shot examples would improve consistency on edge cases.
- **No cross-session memory:** Chat history is maintained within a session (sent from the frontend per turn) but is not persisted across browser reloads or separate sessions.
- **Voice bot:** Real-time speech-to-text + text-to-speech layer could be added as a v2 feature without changing the core agent logic.

---

## 🧪 Test Suite

Run the end-to-end test suite in `apart_agent.ipynb` (Cell 8):

| Test | Input | Expected Score | Telegram | Email |
|------|-------|---------------|----------|-------|
| 1 | Price question | WARM | ❌ | ✅ |
| 2 | Budget + payment plan | HOT | ✅ | ❌ |
| 3 | Building regulations | WARM | ❌ | ✅ |
| 4 | Just browsing | COLD | ❌ | ❌ |

---

## 📦 Requirements

```
langchain
langchain-openai
langchain-pinecone
langchain-community
langgraph
pinecone-client
flask
python-dotenv
requests
ddgs
hunter-python
```

Full list in `requirements.txt`.

---

## 📄 License

Solo project — IronHack AI Bootcamp 2025. Not for commercial use.
