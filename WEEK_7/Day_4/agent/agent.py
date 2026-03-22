"""
Fleet Cost Intelligence Agent
LangGraph agent for Chleo SME — Regional Haulage, Spain
Compatible with langchain-core >= 1.0, langchain-community >= 0.4
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langsmith import traceable
import pandas as pd

load_dotenv()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def _load_costs():
    df = pd.read_csv(os.path.join(DATA_PATH, "processed_costs.csv"))
    df["Date"] = pd.to_datetime(df["Date"])
    for col in ["Fuel", "Maintenance", "Tolls", "Fixed Costs", "Total Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Truck ID"] = df["Truck ID"].astype(str).str.strip()
    df["Driver ID"] = df["Driver ID"].astype(str).str.strip()
    return df

def _load_drivers():
    df = pd.read_csv(os.path.join(DATA_PATH, "dim_drivers.csv"))
    df["Driver ID"] = df["Driver ID"].astype(str).str.strip()
    return df

def _load_vehicles():
    df = pd.read_csv(os.path.join(DATA_PATH, "dim_vehicles.csv"))
    df["Truck ID"] = df["Truck ID"].astype(str).str.strip()
    return df

@tool
def get_fleet_summary(period: str = "all") -> str:
    """Get high-level fleet performance summary. period options: all, 2018, 2019"""
    df = _load_costs()
    if period in ("2018", "2019"):
        df = df[df["Date"].dt.year == int(period)]
    total_fuel = df["Fuel"].sum()
    total_cost = df["Total Cost"].sum()
    fleet_size = df["Truck ID"].nunique()
    months     = df["Date"].nunique()
    fuel_pct   = (total_fuel / total_cost * 100).round(1)
    return (
        f"Fleet summary ({period}): {fleet_size} trucks, {months} months. "
        f"Total fuel: €{total_fuel:,.0f} ({fuel_pct}% of total cost €{total_cost:,.0f}). "
        f"Monthly fleet avg fuel: €{(total_fuel/months):,.0f}."
    )

@tool
def get_fuel_anomalies(threshold_pct: float = 20.0) -> str:
    """Find trucks burning more than threshold_pct above monthly fleet average."""
    df = _load_costs()
    monthly_avg = df.groupby("Date")["Fuel"].mean()
    df = df.copy()
    df["monthly_avg"] = df["Date"].map(monthly_avg)
    df["pct_above"] = ((df["Fuel"] - df["monthly_avg"]) / df["monthly_avg"] * 100).round(1)
    anomalies = df[df["pct_above"] > threshold_pct].sort_values("pct_above", ascending=False)
    if anomalies.empty:
        return f"No anomalies above {threshold_pct}% threshold."
    lines = [f"{len(anomalies)} anomalous records (>{threshold_pct}% above avg):"]
    for _, r in anomalies.head(5).iterrows():
        lines.append(f"Truck {r['Truck ID']} | {r['Date'].strftime('%b %Y')} | €{r['Fuel']:,.0f} | {r['pct_above']:.0f}% above avg")
    return "\n".join(lines)

@tool
def get_top_fuel_trucks(n: int = 5) -> str:
    """Get top n trucks ranked by total fuel spend."""
    df = _load_costs()
    vehicles = _load_vehicles()
    ranked = (
        df.groupby("Truck ID")["Fuel"]
        .agg(total="sum", monthly_avg="mean")
        .reset_index()
        .merge(vehicles[["Truck ID", "Brand", "Truck Type"]], on="Truck ID", how="left")
        .nlargest(n, "total")
    )
    fleet_avg = df["Fuel"].mean()
    lines = [f"Top {n} trucks by fuel:"]
    for i, (_, r) in enumerate(ranked.iterrows(), 1):
        pct = ((r["monthly_avg"] - fleet_avg) / fleet_avg * 100).round(0)
        lines.append(f"{i}. Truck {r['Truck ID']} — Total €{r['total']:,.0f} | Monthly avg €{r['monthly_avg']:,.0f} ({pct:+.0f}%)")
    return "\n".join(lines)

@tool
def get_monthly_fuel_trend(year: str = "all") -> str:
    """Analyze monthly fuel cost trend. year options: all, 2018, 2019"""
    df = _load_costs()
    if year != "all":
        df = df[df["Date"].dt.year == int(year)]
    monthly = df.groupby("Date")["Fuel"].sum().reset_index().sort_values("Date")
    peak   = monthly.loc[monthly["Fuel"].idxmax()]
    trough = monthly.loc[monthly["Fuel"].idxmin()]
    lines  = [f"Fuel trend ({year}): Peak {peak['Date'].strftime('%b %Y')} €{peak['Fuel']:,.0f} | Low {trough['Date'].strftime('%b %Y')} €{trough['Fuel']:,.0f}"]
    for _, r in monthly.iterrows():
        lines.append(f"  {r['Date'].strftime('%b %Y')}: €{r['Fuel']:,.0f}")
    return "\n".join(lines)

@tool
def get_driver_performance() -> str:
    """Compare driver fuel efficiency."""
    df = _load_costs()
    drivers = _load_drivers()
    stats = (
        df.groupby("Driver ID")["Fuel"].agg(avg="mean", total="sum")
        .reset_index()
        .merge(drivers, on="Driver ID", how="left")
        .sort_values("avg", ascending=False)
    )
    fleet_avg = stats["avg"].mean()
    best  = stats.iloc[-1]
    worst = stats.iloc[0]
    lines = [
        f"Driver performance (fleet avg €{fleet_avg:,.0f}/mo):",
        f"Best:  {best.get('Driver', best['Driver ID'])} €{best['avg']:,.0f}/mo",
        f"Worst: {worst.get('Driver', worst['Driver ID'])} €{worst['avg']:,.0f}/mo ({((worst['avg']-fleet_avg)/fleet_avg*100):+.0f}%)",
    ]
    return "\n".join(lines)

@tool
def get_cost_breakdown() -> str:
    """Get total cost breakdown by category."""
    df = _load_costs()
    fuel  = df["Fuel"].sum()
    maint = df["Maintenance"].sum()
    tolls = df["Tolls"].sum()
    fixed = df["Fixed Costs"].sum()
    total = df["Total Cost"].sum()
    return (
        f"Cost breakdown: Fixed {fixed/total*100:.1f}% €{fixed:,.0f} | "
        f"Fuel {fuel/total*100:.1f}% €{fuel:,.0f} | "
        f"Maintenance {maint/total*100:.1f}% €{maint:,.0f} | "
        f"Tolls {tolls/total*100:.1f}% €{tolls:,.0f} | "
        f"5% fuel cut = €{fuel*0.05:,.0f} saved"
    )

SYSTEM_PROMPT = """You are an AI fleet cost analyst for Chleo SME, a regional haulage company in Spain with 50 trucks.
Generate clear, specific, actionable insights. Always mention exact truck IDs, dates, percentages.
Every insight must include a concrete next step. Keep language simple."""

tools = [get_fleet_summary, get_fuel_anomalies, get_top_fuel_trucks,
         get_monthly_fuel_trend, get_driver_performance, get_cost_breakdown]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=os.getenv("OPENAI_API_KEY"))
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

@traceable(name="fleet-insight-agent")
def run_agent(query: str) -> str:
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    return result["messages"][-1].content

@traceable(name="weekly-fleet-report")
def generate_weekly_report() -> None:
    queries = [
        "Give me a fleet performance summary focusing on fuel costs.",
        "Which trucks have the highest fuel costs above fleet average? Top 3.",
        "Is fuel consumption trending up or down and why?",
        "Which drivers have the best and worst fuel efficiency?",
        "What is the single most impactful action to reduce fuel costs this week?",
    ]
    print("\n=== WEEKLY FLEET INTELLIGENCE REPORT ===\n")
    for i, q in enumerate(queries, 1):
        print(f"[{i}] {q}")
        print(run_agent(q))
        print()

if __name__ == "__main__":
    print("Fleet Cost Intelligence Agent — Chleo SME")
    print("Type 'report' for weekly report | 'quit' to exit\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "report":
            generate_weekly_report()
        else:
            print(f"\nAgent: {run_agent(user_input)}\n")
