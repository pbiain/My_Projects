# AI Content Creator

Project scaffold for an AI-powered content creation workflow.

## 📁 Project Structure

```text
ai-content-creator/
├── src/
│   ├── interface.py           # UI Layer: Terminal interactions & formatting
│   ├── main.py                # Orchestrator: Connects all modules
│   ├── prompt_templates.py    # Strategy: Content engines & anti-slop rules
│   ├── knowledge_base.py      # Data: Primary/Secondary KB management
│   ├── document_processor.py  # Ingestion: Markdown processing logic
│   └── llm_integration.py     # Integration: Provider Factory (GPT/Claude)
├── knowledge_base/            # Source Material (.md files)
├── requirements.txt           # Project Dependencies
└── .env                       # API Credentials 