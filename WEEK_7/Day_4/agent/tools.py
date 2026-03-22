"""
Fleet Cost Intelligence Tools
LangChain tools for analyzing Chleo SME fleet data
Each tool is traceable via LangSmith
"""

import os
import pandas as pd
import numpy as np
from langchain.tools import tool
from langsmith import traceable

# Load data once at module level
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def _load_costs() -> pd.DataFrame:
    """Load and prepare the processed costs dataset."""
    df = pd.read_csv(os.path.join(DATA_PATH, "processed_costs.csv"))
    df["Date"] = pd.to_datetime(df["Date"])
    for col in ["Fuel", "Maintenance", "Tolls", "Fixed Costs", "Total Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Truck ID"] = df["Truck ID"].astype(str).str.strip()
    df["Driver ID"] = df["Driver ID"].astype(str).str.strip()
    return df

def _load_drivers() -> pd.DataFrame:
    """Load driver dimension table."""
    return pd.read_csv(os.path.join(DATA_PATH, "dim_drivers.csv"))

def _load_vehicles() -> pd.DataFrame:
    """Load vehicle dimension table."""
    df = pd.read_csv(os.path.join(DATA_PATH, "dim_vehicles.csv"))
    df["Truck ID"] = df["Truck ID"].astype(str).str.strip()
    return df


@tool
@traceable(name="get_fleet_summary")
def get_fleet_summary(period: str = "all") -> str:
    """
    Get a high-level summary of fleet performance.
    
    Args:
        period: Time period to analyze. Options: 'all', '2018', '2019'
    
    Returns:
        Summary string with key fleet metrics
    """
    df = _load_costs()
    
    if period == "2018":
        df = df[df["Date"].dt.year == 2018]
    elif period == "2019":
        df = df[df["Date"].dt.year == 2019]
    
    total_fuel = df["Fuel"].sum()
    total_cost = df["Total Cost"].sum()
    avg_fuel_per_truck = df.groupby("Truck ID")["Fuel"].sum().mean()
    fleet_size = df["Truck ID"].nunique()
    months_covered = df["Date"].nunique()
    fuel_pct = (total_fuel / total_cost * 100).round(1)
    
    return f"""Fleet Summary ({period}):
- Fleet size: {fleet_size} trucks
- Months covered: {months_covered}
- Total fuel spend: €{total_fuel:,.0f}
- Total operating cost: €{total_cost:,.0f}
- Fuel as % of total cost: {fuel_pct}%
- Average fuel per truck (total period): €{avg_fuel_per_truck:,.0f}
- Monthly fleet average fuel: €{(total_fuel / months_covered):,.0f}"""


@tool
@traceable(name="get_fuel_anomalies")
def get_fuel_anomalies(threshold_pct: float = 20.0) -> str:
    """
    Identify trucks with fuel costs significantly above fleet average.
    
    Args:
        threshold_pct: Percentage above average to flag as anomaly (default 20%)
    
    Returns:
        List of anomalous trucks with details
    """
    df = _load_costs()
    
    # Calculate monthly fleet average
    monthly_avg = df.groupby("Date")["Fuel"].mean()
    
    # Join back to main df
    df = df.copy()
    df["monthly_avg"] = df["Date"].map(monthly_avg)
    df["pct_above_avg"] = ((df["Fuel"] - df["monthly_avg"]) / df["monthly_avg"] * 100).round(1)
    
    # Filter anomalies
    anomalies = df[df["pct_above_avg"] > threshold_pct].copy()
    anomalies = anomalies.sort_values("pct_above_avg", ascending=False)
    
    if anomalies.empty:
        return f"No trucks found with fuel costs more than {threshold_pct}% above monthly average."
    
    result = f"Fuel anomalies (>{threshold_pct}% above monthly average):\n"
    result += f"Total anomalous records: {len(anomalies)}\n\n"
    
    # Top 5 worst
    top5 = anomalies.head(5)
    for _, row in top5.iterrows():
        result += f"- Truck {row['Truck ID']} | {row['Date'].strftime('%B %Y')} | "
        result += f"Fuel: €{row['Fuel']:,.0f} | "
        result += f"{row['pct_above_avg']:.0f}% above average\n"
    
    return result


@tool
@traceable(name="get_top_fuel_trucks")
def get_top_fuel_trucks(n: int = 5) -> str:
    """
    Get the trucks with highest total fuel consumption ranked.
    
    Args:
        n: Number of trucks to return (default 5)
    
    Returns:
        Ranked list of highest fuel consuming trucks
    """
    df = _load_costs()
    vehicles = _load_vehicles()
    
    truck_fuel = df.groupby("Truck ID").agg(
        total_fuel=("Fuel", "sum"),
        avg_monthly_fuel=("Fuel", "mean"),
        months=("Date", "count")
    ).reset_index()
    
    truck_fuel = truck_fuel.merge(vehicles[["Truck ID", "Brand", "Truck Type", "Year"]], 
                                   on="Truck ID", how="left")
    truck_fuel = truck_fuel.nlargest(n, "total_fuel")
    
    fleet_avg = df["Fuel"].mean()
    
    result = f"Top {n} highest fuel consuming trucks:\n\n"
    for i, (_, row) in enumerate(truck_fuel.iterrows(), 1):
        pct_above = ((row["avg_monthly_fuel"] - fleet_avg) / fleet_avg * 100).round(1)
        result += f"{i}. Truck {row['Truck ID']} ({row.get('Brand', 'N/A')} {row.get('Truck Type', 'N/A')}, {row.get('Year', 'N/A')})\n"
        result += f"   Total fuel: €{row['total_fuel']:,.0f} | "
        result += f"Monthly avg: €{row['avg_monthly_fuel']:,.0f} | "
        result += f"{pct_above:+.0f}% vs fleet avg\n"
    
    return result


@tool
@traceable(name="get_monthly_fuel_trend")
def get_monthly_fuel_trend(year: str = "all") -> str:
    """
    Analyze fuel cost trends over time.
    
    Args:
        year: Year to analyze. Options: 'all', '2018', '2019'
    
    Returns:
        Monthly fuel trend analysis
    """
    df = _load_costs()
    
    if year != "all":
        df = df[df["Date"].dt.year == int(year)]
    
    monthly = df.groupby("Date").agg(
        total_fuel=("Fuel", "sum"),
        truck_count=("Truck ID", "nunique")
    ).reset_index()
    monthly = monthly.sort_values("Date")
    monthly["fuel_per_truck"] = (monthly["total_fuel"] / monthly["truck_count"]).round(0)
    
    # Find peak and trough
    peak = monthly.loc[monthly["total_fuel"].idxmax()]
    trough = monthly.loc[monthly["total_fuel"].idxmin()]
    
    # Calculate trend
    if len(monthly) > 1:
        first_half = monthly.head(len(monthly)//2)["total_fuel"].mean()
        second_half = monthly.tail(len(monthly)//2)["total_fuel"].mean()
        trend = "increasing" if second_half > first_half else "decreasing"
        trend_pct = abs((second_half - first_half) / first_half * 100).round(1)
    else:
        trend = "insufficient data"
        trend_pct = 0
    
    result = f"Monthly fuel trend ({year}):\n\n"
    result += f"Overall trend: {trend} ({trend_pct}% change first vs second half)\n"
    result += f"Peak month: {peak['Date'].strftime('%B %Y')} — €{peak['total_fuel']:,.0f}\n"
    result += f"Lowest month: {trough['Date'].strftime('%B %Y')} — €{trough['total_fuel']:,.0f}\n\n"
    result += "Monthly breakdown:\n"
    
    for _, row in monthly.iterrows():
        result += f"- {row['Date'].strftime('%b %Y')}: €{row['total_fuel']:,.0f} fleet total | €{row['fuel_per_truck']:,.0f} per truck\n"
    
    return result


@tool
@traceable(name="get_driver_performance")
def get_driver_performance(metric: str = "fuel") -> str:
    """
    Analyze driver performance by cost metrics.
    
    Args:
        metric: Metric to rank by. Options: 'fuel', 'total_cost', 'maintenance'
    
    Returns:
        Driver performance ranking with insights
    """
    df = _load_costs()
    drivers = _load_drivers()
    
    driver_stats = df.groupby("Driver ID").agg(
        avg_fuel=("Fuel", "mean"),
        total_fuel=("Fuel", "sum"),
        avg_total_cost=("Total Cost", "mean"),
        avg_maintenance=("Maintenance", "mean"),
        months=("Date", "count")
    ).reset_index()
    
    driver_stats = driver_stats.merge(
        drivers.rename(columns={"Driver ID": "Driver ID"}), 
        on="Driver ID", how="left"
    )
    
    col_map = {"fuel": "avg_fuel", "total_cost": "avg_total_cost", "maintenance": "avg_maintenance"}
    sort_col = col_map.get(metric, "avg_fuel")
    
    driver_stats = driver_stats.sort_values(sort_col, ascending=False)
    fleet_avg_fuel = driver_stats["avg_fuel"].mean()
    
    result = f"Driver performance ranked by {metric}:\n\n"
    result += f"Fleet average monthly fuel: €{fleet_avg_fuel:,.0f}\n\n"
    
    # Best and worst
    best = driver_stats.iloc[-1]
    worst = driver_stats.iloc[0]
    
    result += f"Best performer: {best.get('Driver', f'Driver {best[\"Driver ID\"]}')} — "
    result += f"Avg fuel €{best['avg_fuel']:,.0f}/month ({((best['avg_fuel']-fleet_avg_fuel)/fleet_avg_fuel*100):.0f}% vs avg)\n"
    
    result += f"Needs attention: {worst.get('Driver', f'Driver {worst[\"Driver ID\"]}')} — "
    result += f"Avg fuel €{worst['avg_fuel']:,.0f}/month ({((worst['avg_fuel']-fleet_avg_fuel)/fleet_avg_fuel*100):+.0f}% vs avg)\n\n"
    
    result += "Full ranking (top 5 by fuel cost):\n"
    for i, (_, row) in enumerate(driver_stats.head(5).iterrows(), 1):
        name = row.get("Driver", f"Driver {row['Driver ID']}")
        pct = ((row["avg_fuel"] - fleet_avg_fuel) / fleet_avg_fuel * 100).round(0)
        result += f"{i}. {name}: €{row['avg_fuel']:,.0f}/month ({pct:+.0f}% vs avg)\n"
    
    return result


@tool
@traceable(name="get_cost_breakdown")
def get_cost_breakdown(group_by: str = "total") -> str:
    """
    Get breakdown of costs by category (fuel, maintenance, tolls, fixed costs).
    
    Args:
        group_by: How to group. Options: 'total', 'monthly', 'truck'
    
    Returns:
        Cost breakdown analysis
    """
    df = _load_costs()
    
    if group_by == "monthly":
        breakdown = df.groupby("Date").agg(
            fuel=("Fuel", "sum"),
            maintenance=("Maintenance", "sum"),
            tolls=("Tolls", "sum"),
            fixed=("Fixed Costs", "sum"),
            total=("Total Cost", "sum")
        ).reset_index()
        
        result = "Monthly cost breakdown:\n\n"
        for _, row in breakdown.iterrows():
            result += f"{row['Date'].strftime('%b %Y')}: "
            result += f"Fuel €{row['fuel']:,.0f} | "
            result += f"Fixed €{row['fixed']:,.0f} | "
            result += f"Maint €{row['maintenance']:,.0f} | "
            result += f"Tolls €{row['tolls']:,.0f}\n"
        
    elif group_by == "truck":
        breakdown = df.groupby("Truck ID").agg(
            fuel=("Fuel", "sum"),
            maintenance=("Maintenance", "sum"),
            tolls=("Tolls", "sum"),
            fixed=("Fixed Costs", "sum"),
            total=("Total Cost", "sum")
        ).reset_index().nlargest(5, "fuel")
        
        result = "Cost breakdown — top 5 trucks by fuel:\n\n"
        for _, row in breakdown.iterrows():
            fuel_pct = (row["fuel"] / row["total"] * 100).round(0)
            result += f"Truck {row['Truck ID']}: Fuel €{row['fuel']:,.0f} ({fuel_pct:.0f}% of total) | "
            result += f"Fixed €{row['fixed']:,.0f} | Maint €{row['maintenance']:,.0f}\n"
    
    else:  # total
        total_fuel = df["Fuel"].sum()
        total_maint = df["Maintenance"].sum()
        total_tolls = df["Tolls"].sum()
        total_fixed = df["Fixed Costs"].sum()
        grand_total = df["Total Cost"].sum()
        
        result = "Total cost breakdown (all periods):\n\n"
        result += f"Fixed costs: €{total_fixed:,.0f} ({total_fixed/grand_total*100:.1f}%)\n"
        result += f"Fuel:        €{total_fuel:,.0f} ({total_fuel/grand_total*100:.1f}%)\n"
        result += f"Maintenance: €{total_maint:,.0f} ({total_maint/grand_total*100:.1f}%)\n"
        result += f"Tolls:       €{total_tolls:,.0f} ({total_tolls/grand_total*100:.1f}%)\n"
        result += f"TOTAL:       €{grand_total:,.0f}\n\n"
        result += f"Key insight: Fuel represents {total_fuel/grand_total*100:.1f}% of costs — "
        result += f"a 5% reduction saves €{total_fuel*0.05:,.0f}"
    
    return result
