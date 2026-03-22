import os
from dotenv import load_dotenv
from langsmith import Client
from openai import OpenAI
import pandas as pd

load_dotenv()

# Initialize clients
langsmith_client = Client()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load processed costs data
df = pd.read_csv("data/processed/processed_costs.csv")

# Sample 10 representative rows for dataset
# Pick rows with high fuel anomalies for interesting insights
df['Date'] = pd.to_datetime(df['Date'])
df = df.dropna(subset=['Fuel', 'Total Cost'])
df['Fuel_pct'] = (df['Fuel'] / df['Total Cost'] * 100).round(2)

# Select 10 diverse examples
samples = df.nlargest(10, 'Fuel').reset_index(drop=True)

def generate_insight(row):
    """Generate an AI insight for a given truck cost record."""
    prompt = f"""You are an AI analyst for a Spanish regional haulage company called Chleo SME.
    
Analyze this monthly truck cost record and generate a concise, actionable business insight in 2-3 sentences.
Focus on fuel efficiency, cost anomalies, and recommendations for the operations manager.

Data:
- Date: {row['Date'].strftime('%B %Y') if pd.notna(row['Date']) else 'Unknown'}
- Truck ID: {row['Truck ID']}
- Driver ID: {row['Driver ID']}
- Distance driven: {row['Distance (Km)']} km
- Fuel cost: €{row['Fuel']:.2f}
- Maintenance cost: €{row['Maintenance']:.2f}
- Total cost: €{row['Total Cost']:.2f}
- Fuel as % of total cost: {row['Fuel_pct']}%

Generate a clear, actionable insight for the fleet operations manager."""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# Generate insights for all 10 samples
print("Generating insights...")
examples = []
for idx, row in samples.iterrows():
    print(f"Generating insight {idx + 1}/10 for Truck {row['Truck ID']}...")
    insight = generate_insight(row)
    
    examples.append({
        "input": {
            "truck_id": str(row['Truck ID']),
            "driver_id": str(row['Driver ID']),
            "date": str(row['Date'].strftime('%B %Y') if pd.notna(row['Date']) else 'Unknown'),
            "distance_km": int(row['Distance (Km)']),
            "fuel_cost": float(row['Fuel']),
            "maintenance_cost": float(row['Maintenance']),
            "total_cost": float(row['Total Cost']),
            "fuel_pct_of_total": float(row['Fuel_pct'])
        },
        "output": insight
    })
    print(f"Insight: {insight[:100]}...")
    print()

# Create LangSmith dataset
dataset_name = "chleo-fuel-intelligence-insights"
print(f"Creating LangSmith dataset: {dataset_name}")

dataset = langsmith_client.create_dataset(
    dataset_name=dataset_name,
    description="AI-generated fuel cost insights for Chleo SME regional haulage fleet. Each example contains monthly truck cost data as input and an actionable business insight as output. Used for Project 5 - BI Dashboard Mini Project."
)

# Add examples to dataset
for example in examples:
    langsmith_client.create_example(
        inputs=example["input"],
        outputs={"insight": example["output"]},
        dataset_id=dataset.id
    )

print(f"\nDataset created successfully!")
print(f"Dataset name: {dataset_name}")
print(f"Dataset ID: {dataset.id}")
print(f"Total examples: {len(examples)}")
print(f"\nView your dataset at: https://smith.langchain.com")
