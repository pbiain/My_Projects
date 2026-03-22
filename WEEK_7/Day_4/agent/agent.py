"""
Fleet Cost Intelligence Agent
LangChain/LangGraph agent for Chleo SME — Regional Haulage, Spain
Generates actionable fuel cost insights from fleet data
"""

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable
from tools import (
    get_fleet_summary,
    get_fuel_anomalies,
    get_top_fuel_trucks,
    get_monthly_fuel_trend,
    get_driver_performance,
    get_cost_breakdown
)

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

# System prompt — focused on Chleo's context
SYSTEM_PROMPT = """You are an AI fleet cost analyst for Chleo SME, a regional haulage company in Spain operating 50 trucks.

Your role is to analyze fleet cost data and generate clear, actionable insights for the operations manager and CEO.

Key context:
- Fuel costs represent ~30-35% of total operating costs
- Net margin is only 2-3% — every euro saved in fuel drops directly to net income
- Chleo is skeptical about AI — always explain your reasoning clearly
- The company uses synthetic TMS and fuel card data (2018-2019)
- Fleet average fuel cost per month: ~€3,057

When generating insights:
1. Be specific — mention exact truck IDs, dates, and percentages
2. Be actionable — every insight must suggest a concrete next step
3. Be transparent — explain what data you used and why you flagged it
4. Keep language simple — the audience is an operations manager, not a data scientist

Available tools:
- get_fleet_summary: Overview of entire fleet performance
- get_fuel_anomalies: Trucks burning above threshold
- get_top_fuel_trucks: Highest fuel consumers ranked
- get_monthly_fuel_trend: Fuel cost over time
- get_driver_performance: Cost metrics per driver
- get_cost_breakdown: Split of fuel, maintenance, tolls, fixed costs
"""

# Build prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Tools list
tools = [
    get_fleet_summary,
    get_fuel_anomalies,
    get_top_fuel_trucks,
    get_monthly_fuel_trend,
    get_driver_performance,
    get_cost_breakdown
]

# Create agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)


@traceable(name="fleet-insight-agent")
def run_agent(query: str, chat_history: list = None) -> str:
    """
    Run the fleet cost intelligence agent.
    
    Args:
        query: Question or request from the operations manager
        chat_history: Previous conversation turns
    
    Returns:
        Agent response with insight and recommendations
    """
    if chat_history is None:
        chat_history = []
    
    result = agent_executor.invoke({
        "input": query,
        "chat_history": chat_history
    })
    
    return result["output"]


@traceable(name="weekly-fleet-report")
def generate_weekly_report() -> dict:
    """
    Generate a complete weekly fleet intelligence report.
    Runs automatically every Monday morning.
    
    Returns:
        Dictionary with insights, anomalies, and recommendations
    """
    print("Generating weekly fleet intelligence report...")
    
    insights = []
    
    # 1. Fleet overview
    overview = run_agent("Give me a summary of overall fleet performance this period. Focus on fuel costs.")
    insights.append({"type": "overview", "insight": overview})
    
    # 2. Anomaly detection
    anomalies = run_agent("Which trucks have the highest fuel costs above fleet average? List the top 3 with specific percentages.")
    insights.append({"type": "anomalies", "insight": anomalies})
    
    # 3. Trend analysis
    trend = run_agent("Is fuel consumption trending up or down over the past few months? What's driving the change?")
    insights.append({"type": "trend", "insight": trend})
    
    # 4. Driver performance
    drivers = run_agent("Which drivers have the best and worst fuel efficiency? What should we do about the worst performer?")
    insights.append({"type": "drivers", "insight": drivers})
    
    # 5. Cost recommendation
    recommendation = run_agent("What is the single most impactful action Chleo could take this week to reduce fuel costs?")
    insights.append({"type": "recommendation", "insight": recommendation})
    
    return {
        "report_type": "weekly_fleet_intelligence",
        "company": "Chleo SME",
        "insights_count": len(insights),
        "insights": insights
    }


if __name__ == "__main__":
    print("Fleet Cost Intelligence Agent — Chleo SME")
    print("=" * 50)
    
    # Interactive mode
    chat_history = []
    print("Ask me anything about the fleet. Type 'report' for full weekly report. Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "report":
            report = generate_weekly_report()
            print("\n=== WEEKLY FLEET INTELLIGENCE REPORT ===")
            for item in report["insights"]:
                print(f"\n[{item['type'].upper()}]")
                print(item["insight"])
            print("\n" + "=" * 50)
        else:
            response = run_agent(user_input, chat_history)
            print(f"\nAgent: {response}\n")
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response))
