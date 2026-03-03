# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Pedro Biain's IRONHACK AI Bootcamp — a 5-week progression from ML fundamentals through agentic systems:
- **Week 1**: ML fundamentals, scikit-learn, Whisper STT/TTS
- **Week 2**: LLM integration, prompt engineering, multi-provider orchestration, RAG
- **Week 3**: LangChain, relevance scoring/rerankers, MCP (Model Context Protocol)
- **Week 4**: LangGraph agentic workflows, ReAct pattern
- **Week 5**: Final project

## Environment Setup

```bash
# Activate virtual environment
source .venv/Scripts/activate   # Windows Git Bash
# or
.venv\Scripts\activate          # Windows CMD

# Install dependencies (from Week 3 onward)
pip install -r WEEK_3/requirements.txt

# Run Jupyter
jupyter notebook
```

API keys are loaded via `.env` files using `python-dotenv`. Required keys: `OPENAI_API_KEY`, `COHERE_API_KEY`, `NEWS_API_KEY`.

## Running Tests

```bash
# Week 2 Day 4 has a pytest suite
cd "WEEK_2/Day 4"
pytest test_summarizer.py -v

# Most validation is done inline in notebooks via test cells
```

## Architecture Patterns

### Multi-Provider LLM with Fallback (Week 2 Day 4)
The news summarizer establishes the canonical pattern used in later weeks:
- `config.py` — centralizes model names, API keys, rate limits
- `llm_providers.py` — `ask_with_fallback()`: tries OpenAI (`gpt-4o-mini`), falls back to Cohere (`command-r7b-12-2024`)
- `CostTracker` class tracks input/output tokens and costs via `tiktoken`; enforces daily budget with 90% warning threshold

### Modular Podcast Generator (Week 2 Day 1)
Three-module separation pattern reused in later projects:
```
src/data_processor.py   # ingests PDF/text input
src/llm_processor.py    # LLM calls, script generation
src/tts_generator.py    # OpenAI TTS output
main.py                 # orchestrates the pipeline
```

### LangGraph Stateful Workflows (Week 4 Day 1)
`StateDict(TypedDict)` carries all mutable fields between nodes. Graph structure: `StateGraph → add_node() → add_conditional_edges() → compile()`. Nodes are pure functions that receive and return state dicts.

### Prompt Engineering Conventions (Week 2 Day 2)
- System message defines a narrow role (classifier, copywriter, parser) — avoid "helpful assistant" default
- Few-shot examples immediately before the task
- Chain-of-Thought before final structured output
- Structured outputs: snake_case field names, explicit max tokens, no markdown in JSON responses
- Measure consistency (std dev across runs), not just binary pass/fail

### Pydantic for Structured LLM Output
All projects from Week 2 onward validate LLM JSON responses with Pydantic v2 models. Always verify with `json.loads()` before Pydantic parsing to catch markdown-wrapped JSON (triple-backtick fenced blocks the model sometimes adds).

## Key Files

| File | Purpose |
|------|---------|
| `WEEK_2/Day 4/config.py` | Reference multi-provider config pattern |
| `WEEK_2/Day 4/llm_providers.py` | Fallback + cost tracking pattern |
| `WEEK_3/requirements.txt` | Canonical dependency list (100+ packages) |
| `WEEK_4/Day_1/normalobjects_langgraph.py` | LangGraph workflow reference |
| `mvp-in-one-hour/claude.md` | MVP project spec template |

## Windows-Specific Notes

- Use UTF-8 encoding explicitly when writing files: `open(f, 'w', encoding='utf-8')`
- Emoji in print statements can cause encoding errors in some terminals — use `rich` library instead
- MCP config lives in `.cursor/mcp.json` (not AppData) for Cursor IDE
- Virtual environment activation differs: `source .venv/Scripts/activate` in Git Bash
