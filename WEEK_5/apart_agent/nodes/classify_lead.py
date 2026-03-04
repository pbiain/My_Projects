import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

LLM_MODEL = "gpt-4o-mini"

CLASSIFICATION_SYSTEM = """
You are a lead scoring assistant for a real estate development in Argentina.
Given the lead's message, classify them as:

HOT  — Any of these signals:
        • Expresses buying intent: "I want to buy", "quiero comprar", "me gustaría comprar", "I'll take it", "I want one"
        • Expresses interest directly: "I'm interested", "estoy interesado", "me interesa"
        • Wants to visit or see the property: "can I see it", "puedo verlo", "me gustaría visitar", "I like it"
        • Mentions a specific budget or asks about financing/payment plans
        • Asks about a specific lot number
        • Mentions investment ROI or asks about returns
WARM — Asks about general prices, availability, lot sizes, or building regulations.
        General curiosity with no clear commitment or purchase-related signal.
COLD — Just browsing, very vague, hypothetical ("what if", "just curious"),
        or shows no real intent signals whatsoever.

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