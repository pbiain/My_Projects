import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

LLM_MODEL = "gpt-4o-mini"

CLASSIFICATION_SYSTEM = """
You are a lead scoring assistant for a real estate development in Argentina.
Given the lead's message, classify them as:

HOT  — Mentions a specific budget, asks about a specific lot number,
        asks about payment plans with intent to buy, mentions investment ROI,
        or signals they are ready to proceed.
WARM — General interest, asking about prices or availability,
        asking about building regulations or construction rules,
        curious but no urgency or budget mentioned.
COLD — Just browsing, very vague, hypothetical, or no real intent signals.

Respond ONLY with valid JSON, no extra text:
{"score": "HOT", "reason": "one sentence explanation"}
"""

classifier_llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

def classify_lead(state):
    response = classifier_llm.invoke([
        SystemMessage(content=CLASSIFICATION_SYSTEM),
        HumanMessage(content=f"Lead message: {state['user_message']}"),
    ])
    try:
        parsed = json.loads(response.content)
        state["lead_score"] = parsed.get("score", "COLD")
        state["score_reason"] = parsed.get("reason", "")
        state["actions_taken"].append(f"classified_as_{state['lead_score']}")
    except json.JSONDecodeError:
        state["lead_score"] = "COLD"
        state["score_reason"] = "parse error"
        state["actions_taken"].append("classification_parse_error")
    return state