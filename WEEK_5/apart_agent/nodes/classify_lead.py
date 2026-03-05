import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

LLM_MODEL = "gpt-4o-mini"

CLASSIFICATION_SYSTEM = """
You are a lead scoring assistant for a real estate development in Argentina.
Given the lead's message, classify them as HOT, WARM, or COLD.

DEFINITIONS:
HOT  — Strong purchase-related signal. Any of:
        • Buying intent: "I want to buy", "quiero comprar", "I'll take it", "lo compro"
        • Direct interest: "I'm interested", "estoy interesado", "me interesa"
        • Wants to visit or see the property: "can I see it", "puedo verlo", "quiero visitar"
        • Asks about payment plans or financing: "payment plan", "cuotas", "formas de pago", "financiamiento"
        • Mentions a specific budget or asks about returns / ROI
        • Asks about a specific lot number
        • Requests contact with an advisor
WARM — General curiosity about the project, no commitment signal. Examples:
        • Asks general price range or availability
        • Asks about lot sizes, amenities, or building regulations
        • Compares sizes or asks "what's the cheapest"
COLD — No real intent. Examples:
        • Just browsing or asking location/access out of pure curiosity
        • Hypothetical questions ("what if", "just wondering")
        • Explicitly uninterested or negative

FEW-SHOT EXAMPLES (follow these exactly):

Lead message: "I'm not interested in this project"
{"score": "COLD", "reason": "The lead explicitly states they are not interested."}

Lead message: "Where is Amarras San Pedro located?"
{"score": "COLD", "reason": "Pure geographic curiosity with no purchase intent."}

Lead message: "Just curious, what kind of project is this?"
{"score": "COLD", "reason": "Vague exploratory question with no buying signal."}

Lead message: "What's your cheapest piece of land?"
{"score": "WARM", "reason": "Asking about price range shows general interest but no commitment."}

Lead message: "How many lots are still available?"
{"score": "WARM", "reason": "Asking about availability indicates curiosity but no clear intent to buy."}

Lead message: "What are the amenities at Amarras San Pedro?"
{"score": "WARM", "reason": "General project inquiry with no purchase-related signal."}

Lead message: "Tell me about the payment plan"
{"score": "HOT", "reason": "Asking about financing/payment plans is a strong indicator of purchase intent."}

Lead message: "Can I see it? I'd like to visit the terrain"
{"score": "HOT", "reason": "Wanting to visit the property is a strong buying signal."}

Lead message: "I have a budget of US$ 80,000, what can I get?"
{"score": "HOT", "reason": "Mentioning a specific budget indicates readiness to purchase."}

Lead message: "I'm interested, how do I contact an advisor?"
{"score": "HOT", "reason": "Directly expressing interest and requesting contact confirms strong purchase intent."}

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