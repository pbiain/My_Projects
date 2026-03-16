"""
Configuration for the LLM-as-judge evaluation system.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
JUDGE_MODEL = "gpt-4o-mini"

MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,   # $0.15 per 1M input tokens
        "output": 0.0006 / 1000,   # $0.60 per 1M output tokens
    },
    "gpt-4o": {
        "input": 0.0025 / 1000,    # $2.50 per 1M input tokens
        "output": 0.01 / 1000,     # $10.00 per 1M output tokens
    },
}
