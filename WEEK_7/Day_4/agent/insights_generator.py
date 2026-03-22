"""
Insight Generator
Batch generation of fleet insights for LangSmith monitoring
Runs weekly to produce insights logged to LangSmith dataset
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client, traceable
from openai import OpenAI

load_dotenv()

langsmith_client = Client()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSIGHT_PROMPTS = [
    {
        "id": "fuel_anomaly",
        "prompt": "Truck 17 consumed €7,828 in fuel last month — 112% above the fleet average of €3,057. Distance driven was 6,579 km. Generate a specific actionable insight for the operations manager.",
        "category": "anomaly_detection"
    },
    {
        "id": "driver_efficiency",
        "prompt": "Driver Ridwan Greaves (Truck 2) averaged €4,200/month in fuel vs fleet average €3,057. Driver Karol Woods (Truck 6) averaged €2,813. What insight can you draw about driver behavior and what should the fleet manager do?",
        "category": "driver_performance"
    },
    {
        "id": "seasonal_trend",
        "prompt": "Fleet fuel spend peaked at €72,356 in October 2018 then dropped to €25,219 in November. This flat period continued through February 2019. What does this pattern suggest and what should Chleo investigate?",
        "category": "trend_analysis"
    },
    {
        "id": "cost_structure",
        "prompt": "Fixed costs represent 64% of total fleet operating costs, fuel 22%, maintenance 8%, tolls 6%. What does this cost structure mean for Chleo's pricing strategy and where should she focus cost reduction efforts?",
        "category": "cost_analysis"
    },
    {
        "id": "roi_projection",
        "prompt": "The fleet spends €901,895 on fuel annually. AI-powered route and driver optimization typically achieves 5-8% fuel reduction for SME fleets. What is the financial impact for Chleo and how should she prioritize implementation?",
        "category": "business_case"
    }
]


@traceable(name="generate-batch-insights", project_name="chleo-fuel-intelligence")
def generate_insights_batch() -> list:
    """
    Generate a batch of fleet insights and log them to LangSmith.
    
    Returns:
        List of generated insights with metadata
    """
    results = []
    
    for prompt_config in INSIGHT_PROMPTS:
        print(f"Generating insight: {prompt_config['id']}...")
        
        insight = _generate_single_insight(
            prompt=prompt_config["prompt"],
            category=prompt_config["category"],
            insight_id=prompt_config["id"]
        )
        
        results.append({
            "id": prompt_config["id"],
            "category": prompt_config["category"],
            "prompt": prompt_config["prompt"],
            "insight": insight,
            "generated_at": datetime.now().isoformat()
        })
        
        print(f"  Generated: {insight[:80]}...")
    
    return results


@traceable(name="single-insight-generation")
def _generate_single_insight(prompt: str, category: str, insight_id: str) -> str:
    """Generate a single insight with LangSmith tracing."""
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an AI fleet cost analyst for Chleo SME, a regional haulage company in Spain.
Generate clear, specific, actionable insights in 2-3 sentences.
Always include: what the data shows, why it matters, and what to do about it.
Use specific numbers. Keep language simple — audience is an operations manager."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content


def save_insights_to_file(insights: list, output_path: str = None):
    """Save generated insights to a JSON file for documentation."""
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "langsmith", "monitoring_results",
            f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(insights, f, indent=2)
    
    print(f"Insights saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Fleet Insight Generator — Chleo SME")
    print("=" * 50)
    print(f"Generating {len(INSIGHT_PROMPTS)} insights...\n")
    
    insights = generate_insights_batch()
    
    print("\n=== GENERATED INSIGHTS ===\n")
    for item in insights:
        print(f"[{item['category'].upper()}] {item['id']}")
        print(f"{item['insight']}")
        print()
    
    # Save to file
    saved_path = save_insights_to_file(insights)
    
    print(f"\nDone. {len(insights)} insights generated and logged to LangSmith.")
    print(f"View at: https://smith.langchain.com")
