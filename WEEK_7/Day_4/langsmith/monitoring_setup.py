import os  # LangSmith monitoring and experiment setup for Chleo SME Project 5
import json
from dotenv import load_dotenv
from langsmith import Client, evaluate
from langsmith.schemas import Run, Example
from openai import OpenAI

load_dotenv()

# Initialize clients
langsmith_client = Client()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATASET_NAME = "chleo-fuel-intelligence-insights"

def generate_insight(inputs: dict) -> dict:
    """Target function: generates a fuel insight from truck cost data."""
    prompt = f"""You are an AI analyst for a Spanish regional haulage company called Chleo SME.

Analyze this monthly truck cost record and generate a concise, actionable business insight in 2-3 sentences.
Focus on fuel efficiency, cost anomalies, and recommendations for the operations manager.

Data:
- Date: {inputs.get('date', 'Unknown')}
- Truck ID: {inputs.get('truck_id', 'Unknown')}
- Driver ID: {inputs.get('driver_id', 'Unknown')}
- Distance driven: {inputs.get('distance_km', 0)} km
- Fuel cost: €{inputs.get('fuel_cost', 0):.2f}
- Maintenance cost: €{inputs.get('maintenance_cost', 0):.2f}
- Total cost: €{inputs.get('total_cost', 0):.2f}
- Fuel as % of total cost: {inputs.get('fuel_pct_of_total', 0)}%

Generate a clear, actionable insight for the fleet operations manager."""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return {"insight": response.choices[0].message.content}


def evaluate_insight_quality(run: Run, example: Example) -> dict:
    """LLM-as-judge evaluator scoring insight quality across 4 criteria."""
    
    generated_insight = run.outputs.get("insight", "")
    input_data = example.inputs
    
    judge_prompt = f"""You are an expert evaluator assessing the quality of AI-generated business insights for a logistics company.

ORIGINAL DATA:
- Date: {input_data.get('date')}
- Truck ID: {input_data.get('truck_id')}
- Fuel Cost: €{input_data.get('fuel_cost')}
- Total Cost: €{input_data.get('total_cost')}
- Fuel % of Total: {input_data.get('fuel_pct_of_total')}%
- Distance: {input_data.get('distance_km')} km

GENERATED INSIGHT:
{generated_insight}

Evaluate this insight on 4 criteria. Return ONLY a JSON object with no markdown:
{{
  "relevance": <score 1-5, does it address the data provided>,
  "accuracy": <score 1-5, are the numbers and facts correct>,
  "actionability": <score 1-5, does it give clear actions for the manager>,
  "clarity": <score 1-5, is it clear and understandable for a non-technical CEO>,
  "overall": <average of the 4 scores>,
  "feedback": "<one sentence explaining the main strength or weakness>"
}}"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0
    )
    
    try:
        scores = json.loads(response.choices[0].message.content)
        return {
            "key": "insight_quality",
            "score": scores.get("overall", 0) / 5,  # Normalize to 0-1
            "value": scores
        }
    except json.JSONDecodeError:
        return {
            "key": "insight_quality", 
            "score": 0.5,
            "value": {"feedback": "Could not parse evaluation"}
        }


def evaluate_actionability(run: Run, example: Example) -> dict:
    """Dedicated evaluator for actionability — most important for Chleo."""
    generated_insight = run.outputs.get("insight", "")
    
    judge_prompt = f"""Does this logistics insight contain a specific, actionable recommendation that an operations manager can act on immediately?

INSIGHT: {generated_insight}

Return ONLY a JSON object with no markdown:
{{
  "score": <1 if actionable, 0 if not>,
  "reason": "<brief explanation>"
}}"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        return {
            "key": "is_actionable",
            "score": result.get("score", 0),
            "value": result.get("reason", "")
        }
    except:
        return {"key": "is_actionable", "score": 0, "value": "Parse error"}


if __name__ == "__main__":
    print("Starting LangSmith experiment...")
    print(f"Dataset: {DATASET_NAME}")
    print()
    
    results = evaluate(
        generate_insight,
        data=DATASET_NAME,
        evaluators=[evaluate_insight_quality, evaluate_actionability],
        experiment_prefix="fuel-insight-evaluation",
        metadata={
            "project": "Project 5 - BI Dashboard",
            "model": "gpt-4o-mini",
            "use_case": "Fuel anomaly insight generation for Chleo SME"
        }
    )
    
    print("\nExperiment completed!")
    print("View results at: https://smith.langchain.com")
    print(f"Dataset: Datasets & Experiments > {DATASET_NAME} > Experiments")
