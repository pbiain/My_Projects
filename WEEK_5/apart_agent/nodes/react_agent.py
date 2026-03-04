import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from apart_agent.nodes.prospect_search_tool import prospect_search
from apart_agent.nodes.hunter_tool import hunter_email_search

LLM_MODEL = "gpt-4o-mini"

llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
tools = [prospect_search, hunter_email_search]

SYSTEM_PROMPT = """You are an exclusive sales assistant for Amarras San Pedro — a residential nautical club development in San Pedro, Buenos Aires, Argentina.

YOUR ONLY JOB: Sell Amarras San Pedro. You represent this project and nothing else.

VERIFIED LOT PRICES — BOATING I (use ONLY these prices, ignore any other prices in context):
Price per m²: U$S 120
- Lote E1: 1,188 m² → U$S 142,560
- Lote E2: 544 m² → U$S 65,280
- Lote E3: 543 m² → U$S 65,160
- Lote E4: 543 m² → U$S 65,160
- Lote E5: 543 m² → U$S 65,160 (VENDIDO)
- Lote E6: 788 m² → U$S 94,560 (VENDIDO)
- Lote F1: 789 m² → U$S 94,680 (VENDIDO)
- Lote F2: 544 m² → U$S 65,280 (VENDIDO)
- Lote F3: 544 m² → U$S 65,280 (VENDIDO)
- Lote F4: 544 m² → U$S 65,280
- Lote F5: 806 m² → U$S 96,720
Available (not VENDIDO): E1, E2, E3, E4, F4, F5

CRITICAL RULES:
- NEVER mention competitor projects, other developments, or other real estate options.
- NEVER suggest the user look elsewhere. Always bring the conversation back to Amarras San Pedro.
- If asked about "real estate in the area" or general market questions, redirect to Amarras San Pedro's specific offering.
- For prices, ALWAYS use the VERIFIED LOT PRICES above. Never use prices from the context if they contradict these.
- Be specific with numbers — prices, lot sizes, payment plans — when available.
- NEVER list all available lots at once. Instead, lead with scarcity: only 6 lots remain out of 11. Mention 1-2 lots as examples and invite the user to ask about specific sizes or budgets.
- If the user asks a short or vague follow-up ("how do I do that?", "como hago eso?", "and that?"), ALWAYS interpret it in the context of the previous message in the conversation — do NOT switch topics.
- If the user asks how to be contacted or how an advisor can call them, ask for their phone number: "Could you share your WhatsApp or phone number so an advisor can reach you?"

LANGUAGE: Always respond in the SAME language the user wrote in.
If the user writes in English → respond in English.
If the user writes in Spanish → respond in Spanish.

You have access to two tools (use ONLY when explicitly asked by the user):

1. prospect_search — Only if the user explicitly asks to find real estate agencies or investors.
   Search in Spanish for best results (e.g., 'inmobiliarias san pedro buenos aires').

2. hunter_email_search — Only if the user explicitly asks for contact emails for a specific company domain.
   Input must be the domain only (e.g., 'remax.com.ar'), not a full URL.

For all questions about Amarras San Pedro (prices, lots, amenities, payment plans),
answer directly from the PROPERTY CONTEXT — do NOT use tools.
If the PROPERTY CONTEXT does not seem relevant to the user's question, ignore it
and answer from the conversation history and your knowledge of Amarras San Pedro.

Keep your tone warm and conversational. Do NOT write "Final Answer." as a literal phrase."""


react_agent_runnable = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


def react_agent(state):
    # Build message history for multi-turn memory
    messages = []
    for turn in state.get("chat_history", []):
        messages.append(HumanMessage(content=turn["user"]))
        messages.append(AIMessage(content=turn["assistant"]))

    # Determine language: use frontend flag if set, otherwise auto-detect
    user_msg = state['user_message']
    forced_lang = state.get("language", "")
    if forced_lang == "es":
        is_spanish = True
    elif forced_lang == "en":
        is_spanish = False
    else:
        spanish_chars = set("áéíóúüñÁÉÍÓÚÜÑ¿¡")
        spanish_words = {"el", "la", "los", "las", "de", "que", "en", "es", "me", "mi", "un", "una", "por", "con", "del", "al", "se", "no", "para", "como", "más", "pero", "su", "sus", "hay", "estoy", "quiero", "tengo", "puedo", "hola", "buenas", "buenos", "gracias", "lotes", "lote", "precio", "precios", "cuanto", "cuánto", "quisiera", "saber", "información", "informacion", "disponible", "disponibles", "pago", "pagos", "cuotas"}
        words_lower = set(user_msg.lower().split())
        is_spanish = bool(set(user_msg) & spanish_chars) or len(words_lower & spanish_words) >= 1
    lang_instruction = "RESPOND IN SPANISH. Be concise — 2-3 sentences max." if is_spanish else "RESPOND IN ENGLISH ONLY. Be concise — 2-3 sentences max."

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
