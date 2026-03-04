import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from apart_agent.nodes.mercadolibre_tool import prospect_search
from apart_agent.nodes.hunter_tool import hunter_email_search

LLM_MODEL = "gpt-4o-mini"

llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
tools = [prospect_search, hunter_email_search]

SYSTEM_PROMPT = """You are a professional real estate sales assistant for Apart Club San Pedro,
a residential nautical club development in San Pedro, Buenos Aires, Argentina.

CRITICAL: Always respond in the SAME language the user wrote in.
If the user writes in English → respond in English, even if the property context is in Spanish.
If the user writes in Spanish → respond in Spanish.
Be specific with numbers — prices, lot sizes, payment plans — when available in the context.

You have access to two tools:

1. prospect_search — Use this when the user asks to find:
   - Real estate agencies or inmobiliarias in the Buenos Aires / San Pedro area
   - Private investors interested in Argentine real estate
   - Potential buyers or comparable developments
   - Contact information, websites, or phone numbers for leads
   Search in Spanish for best results (e.g., 'inmobiliarias san pedro buenos aires').

2. hunter_email_search — Use this when you have a company domain and need emails.
   Input must be the domain only (e.g., 'remax.com.ar'), not a full URL.
   Use AFTER prospect_search finds an agency website/domain.

For questions about Apart Club San Pedro (prices, lots, regulations, payment plans),
answer directly from the PROPERTY CONTEXT — do NOT use tools.

Keep your tone warm and conversational, but vary how you close each response naturally.
Do NOT write "Final Answer." as a literal phrase in your response."""


react_agent_runnable = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


def react_agent(state):
    # Build message history for multi-turn memory
    messages = []
    for turn in state.get("chat_history", []):
        messages.append(HumanMessage(content=turn["user"]))
        messages.append(AIMessage(content=turn["assistant"]))

    # Detect user language and inject explicit instruction
    user_msg = state['user_message']
    spanish_chars = set("áéíóúüñÁÉÍÓÚÜÑ¿¡")
    spanish_words = {"el", "la", "los", "las", "de", "que", "en", "es", "me", "mi", "un", "una", "por", "con", "del", "al", "se", "no", "para", "como", "más", "pero", "su", "sus", "hay", "estoy", "quiero", "tengo", "puedo"}
    words_lower = set(user_msg.lower().split())
    is_spanish = bool(set(user_msg) & spanish_chars) or len(words_lower & spanish_words) >= 2
    lang_instruction = "RESPOND IN SPANISH." if is_spanish else "RESPOND IN ENGLISH ONLY. Do NOT use Spanish."

    full_input = f"{lang_instruction}\n\nPROPERTY CONTEXT:\n{state['retrieved_context']}\n\n---\nUser: {user_msg}"
    messages.append(HumanMessage(content=full_input))

    result = react_agent_runnable.invoke({"messages": messages})
    response = result["messages"][-1].content

    # Strip the "Final Answer:" label injected by the ReAct framework
    if "Final Answer:" in response:
        response = response.split("Final Answer:")[0].strip()

    state["agent_response"] = response
    state["actions_taken"].append("react_agent")
    return state
