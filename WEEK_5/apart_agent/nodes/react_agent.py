import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

LLM_MODEL = "gpt-4o-mini"

tavily_tool = TavilySearchResults(max_results=3)
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
tools = [tavily_tool]

SYSTEM_PROMPT = """You are a professional real estate sales assistant for Apart Club San Pedro,
a residential nautical club development in San Pedro, Buenos Aires, Argentina.
Answer in the same language as the lead's question (Spanish or English).
Be specific with numbers — prices, lot sizes, payment plans — when available in the context.
Use the tavily_search tool ONLY when the lead asks how prices compare to nearby developments
or asks about the broader real estate market. Do NOT use it for questions answerable from context.
Always end with a clear, professional Final Answer."""

react_agent_runnable = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

def react_agent(state):
    full_input = f"PROPERTY CONTEXT:\n{state['retrieved_context']}\n\n---\nLead question: {state['user_message']}"
    result = react_agent_runnable.invoke({"messages": [HumanMessage(content=full_input)]})
    state["agent_response"] = result["messages"][-1].content
    state["actions_taken"].append("react_agent")
    return state