# Lab Report — Using MCP in LangChain
**Week 3 | Day 5**  
**Start time:** 19:45  
**Total time:** ~2h 20min

---

## Time per Stage

| Stage | Description | Estimated Time |
|---|---|---|
| Step 1 | Setup & package verification | ~25 min |
| Step 2 | Architecture & planning | ~10 min |
| Step 3-4 | Dependency audit & secrets | ~5 min |
| Step 5 | Implementation plan | ~5 min |
| Stage 1 | Project scaffold | ~10 min |
| Stage 2 | MCP connection | ~30 min (debugging) |
| Stage 3 | Load tools into LangChain | ~10 min |
| Stage 4 | Create agent + test queries | ~15 min |
| Stage 5 | MCP resources | ~10 min |
| Stage 6 | Complete document analysis agent | ~20 min |
| **Total** | | **~2h 20min** |

---

## Challenges

### 1. Environment confusion (biggest time sink)
Multiple Python environments coexisted: `.venv`, `ironhack_env`, and global Python.
The terminal kept switching between them silently. The VS Code play button used the
wrong interpreter, causing `ModuleNotFoundError` and silent failures that were hard to trace. I'll try to fix that in my vscode

**Root cause:** No environment diagnostic protocol was established at the start.

### 2. Silent script execution
The script ran and exited with zero output and zero error message.
This was caused by the wrong Python interpreter being used — the script
couldn't even reach the first `print()` statement.

**Root cause:** Missing `traceback.print_exc()` and no upfront interpreter validation.

### 3. API changes in langchain-mcp-adapters
`MultiServerMCPClient` no longer supports `async with` as of version 0.1.0.
The error message was clear once visible — the challenge was getting to it
through the silent failure layer.

### 4. Emoji encoding on Windows
PowerShell's default encoding (cp1252) cannot handle emojis when redirecting
output to a file. Fixed by removing emojis from all print statements.

---

## What I Can Improve

- Always run an **environment diagnostic** at the start of every lab:
  - `python -c "import sys; print(sys.executable)"`
  - Test a key import before writing any code
- Add `traceback.print_exc()` from the beginning so errors are never silent
- Build and test a **minimal version** of the script before adding complexity
- Be more aware of which interpreter VS Code is using before running anything

---

## Things to Learn More About in the Future

- **Python virtual environments** — how `.venv`, conda, and global Python interact
  and how to manage them cleanly across projects
- **`asyncio` and `async/await`** — why MCP requires async, how the event loop works,
  and common pitfalls on Windows
- **ReAct agent pattern** — how the agent reasons, calls tools, observes results,
  and repeats until it reaches a final answer
- **MCP protocol** — the difference between tools (actions) and resources (context),
  and how different MCP servers expose them differently
- **Windows terminal encoding** — why special characters break output redirection
  and how to configure UTF-8 encoding properly in PowerShell

## Questions I asked so I could understand things better
---
## Note on Langraph 

- Where it appears:

1. create_react_agent comes from LangGraph
pythonfrom langgraph.prebuilt import create_react_agent
Even though it feels like a LangChain function, it's actually a LangGraph prebuilt component. That's why I got the deprecation warning saying it moved.
2. The agent itself runs on LangGraph
When I call agent.ainvoke(), under the hood LangGraph is managing the agent's execution as a graph with nodes and edges:

This is the graph

[START]

   ↓

[LLM thinks] → decides to call a tool

   ↓

[Tool executes] → returns result

   ↓

[LLM thinks again] → has enough info?

   ↓ No              ↓ Yes

[call another tool]  [give final answer]

↓

[END]

3. The ReAct pattern is a LangGraph graph
The ReAct loop (Reason → Act → Observe → Repeat) is literally implemented as a state machine graph in LangGraph.

So in simple terms:

LangChain provides the tools, LLM wrapper, and abstractions
LangGraph provides the agent execution engine that orchestrates the loop
MCP provides the actual capabilities (read files, list directories, etc.)

They work together — LangGraph is the engine, LangChain is the framework, MCP is the toolbox.


## Note on Cursor vs Python

The previous lab focused on setting up MCP in Cursor from the **user side** —
configuring the server so Cursor's AI could use it automatically.

This lab approached MCP from the **developer side** — building my own agent in Python that connects to MCP programmatically using LangChain.

Cursor abstracts all of this away. Here I wired it up myself, which is harder but much more educational. Now I understand what Cursor is doing under the hood.

---

## Final Result

| Objective | Status |
|---|---|
| Connect to MCP server | Done |
| Load MCP tools into LangChain | Done |
| Build ReAct agent with MCP tools | Done |
| Access MCP resources | Done (filesystem server does not support them) |
| Complete document analysis agent | Done |
| Code is well documented | Done |
