# ============================================================
# CELL 1 - Imports
# ============================================================
import traceback
from datetime import datetime
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# ============================================================
# CELL 2 - Load environment and start timer
# ============================================================
load_dotenv()

START_TIME = datetime.now()
print(f"[START] Lab started at: {START_TIME.strftime('%H:%M:%S')}")

# ============================================================
# CELL 3 - Initialize the LLM
# ============================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ============================================================
# CELL 4 - STATE
# This dictionary is passed through every node
# Think of it as the "file" for each complaint
# ============================================================
class ComplaintState(TypedDict):
    complaint: str        # The original complaint text
    category: str         # portal, monster, psychic, environmental, other
    is_valid: bool        # Did it pass validation?
    investigation: str    # What we found during investigation
    resolution: str       # The proposed fix
    closure_summary: str  # Final wrap-up
    workflow_path: List[str]  # Tracks which nodes we've visited
    status: str           # Current step name


    # ============================================================
# CELL 5 - INTAKE NODE
# Job: Read the complaint and categorize it into one of 5 categories
# Fills in: state["category"]
# ============================================================
def intake_node(state: ComplaintState) -> ComplaintState:
    print("\n[INTAKE] Processing complaint...")
    
    response = llm.invoke([HumanMessage(content=f"""
Categorize this Downside Up complaint into exactly one category:
- portal: Issues with portal timing, location, or behavior
- monster: Issues with creature behavior
- psychic: Issues with psychic abilities
- environmental: Issues with electricity, weather, physical environment
- other: Anything else

Complaint: {state["complaint"]}

Reply with ONLY the category word, nothing else.
""")])
    
    category = response.content.strip().lower()
    print(f"[INTAKE] Category: {category}")
    
    return {
        **state,
        "category": category,
        "workflow_path": state.get("workflow_path", []) + ["intake"],
        "status": "intake"
    }

# ============================================================
# CELL 6 - VALIDATE NODE
# Job: Check if the complaint has enough detail to proceed
# Fills in: state["is_valid"]
# ============================================================
def validate_node(state: ComplaintState) -> ComplaintState:
    print("\n[VALIDATE] Validating complaint...")
    
    response = llm.invoke([HumanMessage(content=f"""
Does this complaint have enough detail to investigate?
Category: {state["category"]}
Complaint: {state["complaint"]}

Reply with ONLY yes or no.
""")])
    
    is_valid = response.content.strip().lower() == "yes"
    print(f"[VALIDATE] Valid: {is_valid}")
    
    return {
        **state,
        "is_valid": is_valid,
        "workflow_path": state["workflow_path"] + ["validate"],
        "status": "validate"
    }

# ============================================================
# CELL 7 - INVESTIGATE NODE
# Job: Gather information based on the category
# Fills in: state["investigation"]
# ============================================================
def investigate_node(state: ComplaintState) -> ComplaintState:
    print("\n[INVESTIGATE] Investigating...")
    
    response = llm.invoke([HumanMessage(content=f"""
You are investigating a Downside Up complaint.
Category: {state["category"]}
Complaint: {state["complaint"]}

Write a brief investigation summary (2-3 sentences).
""")])
    
    print(f"[INVESTIGATE] Done")
    
    return {
        **state,
        "investigation": response.content.strip(),
        "workflow_path": state["workflow_path"] + ["investigate"],
        "status": "investigate"
    }

# ============================================================
# CELL 8 - RESOLVE NODE
# Job: Propose a solution based on the investigation
# Fills in: state["resolution"]
# ============================================================
def resolve_node(state: ComplaintState) -> ComplaintState:
    print("\n[RESOLVE] Creating resolution...")
    
    response = llm.invoke([HumanMessage(content=f"""
Based on this investigation, propose a resolution.
Category: {state["category"]}
Investigation: {state["investigation"]}

Include a predicted effectiveness: high, medium, or low.
Keep it to 2-3 sentences.
""")])
    
    print(f"[RESOLVE] Done")
    
    return {
        **state,
        "resolution": response.content.strip(),
        "workflow_path": state["workflow_path"] + ["resolve"],
        "status": "resolve"
    }

# ============================================================
# CELL 9 - CLOSE NODE
# Job: Wrap everything up into a final summary
# Fills in: state["closure_summary"]
# ============================================================
def close_node(state: ComplaintState) -> ComplaintState:
    print("\n[CLOSE] Closing complaint...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    response = llm.invoke([HumanMessage(content=f"""
Write a closure summary for this complaint.
Category: {state["category"]}
Resolution: {state["resolution"]}
Timestamp: {timestamp}

Keep it to 2 sentences.
""")])
    
    print(f"[CLOSE] Complaint closed at {timestamp}")
    
    return {
        **state,
        "closure_summary": response.content.strip(),
        "workflow_path": state["workflow_path"] + ["close"],
        "status": "closed"
    }


# ============================================================
# CELL 10 - BUILD THE GRAPH
# This is where LangGraph connects all nodes together
# Think of it as drawing the assembly line map
# ============================================================
workflow = StateGraph(ComplaintState)

# Add each node (name, function)
workflow.add_node("intake", intake_node)
workflow.add_node("validate", validate_node)
workflow.add_node("investigate", investigate_node)
workflow.add_node("resolve", resolve_node)
workflow.add_node("close", close_node)

# Define the flow - straight line, one after another
workflow.set_entry_point("intake")
workflow.add_edge("intake", "validate")
workflow.add_edge("validate", "investigate")
workflow.add_edge("investigate", "resolve")
workflow.add_edge("resolve", "close")
workflow.add_edge("close", END)

# Compile - this "locks in" the graph and makes it runnable
app = workflow.compile()

# ============================================================
# CELL 10 - TEST: Just verify the graph compiled correctly
# ============================================================
print("[GRAPH] Workflow compiled successfully!")
print(f"[GRAPH] Nodes: {list(workflow.nodes.keys())}")

# ============================================================
# CELL 11 - TEST THE WORKFLOW
# Run 3 complaints through the full pipeline
# ============================================================
test_complaints = [
    "The Downside Up portal opens at different times each day. How do I predict when?",
    "Demogorgons sometimes work together and sometimes fight. What's their deal?",
    "This is not a valid complaint about something random"  # Should be rejected
]

results = []  # Store results for HTML output

for i, complaint in enumerate(test_complaints, 1):
    print(f"\n{'='*50}")
    print(f"COMPLAINT {i}: {complaint}")
    print('='*50)
    
    result = app.invoke({
        "complaint": complaint,
        "category": "",
        "is_valid": False,
        "investigation": "",
        "resolution": "",
        "closure_summary": "",
        "workflow_path": [],
        "status": ""
    })
    
    results.append(result)  # Save result for HTML
    print(f"[RESULT] Category: {result['category']}")
    print(f"[RESULT] Valid: {result['is_valid']}")
    print(f"[RESULT] Path: {' → '.join(result['workflow_path'])}")

# ============================================================
# CELL 12 - SAVE RESULTS TO HTML
# Opens nicely in your browser instead of reading the terminal
# ============================================================
html_output = """
<html>
<head>
    <style>
        body { font-family: Arial; max-width: 900px; margin: 40px auto; background: #f5f5f5; }
        .complaint { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .category { background: #4a90e2; color: white; padding: 4px 10px; border-radius: 4px; }
        .valid-false { color: red; }
        .valid-true { color: green; }
        .path { background: #f0f0f0; padding: 8px; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
<h1>🌀 Downside Up Complaint Processor</h1>
"""


for i, result in enumerate(results, 1):
    html_output += f"""
    <div class="complaint">
        <h2>Complaint {i}</h2>
        <p><b>Input:</b> {result['complaint']}</p>
        <p><b>Category:</b> <span class="category">{result['category']}</span></p>
        <p><b>Valid:</b> <span class="valid-{str(result['is_valid']).lower()}">{result['is_valid']}</span></p>
        <p><b>Resolution:</b> {result['resolution']}</p>
        <p><b>Closure:</b> {result['closure_summary']}</p>
        <p><b>Path:</b> <span class="path">{' → '.join(result['workflow_path'])}</span></p>
    </div>
    """

html_output += "</body></html>"

with open("results.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("\n[OUTPUT] Done! Open results.html in your browser to see the results!")

# ============================================================
# CELL 13 - VISUALIZE WORKFLOW PATH
# Saves a visual diagram of the graph to the HTML
# ============================================================

# Generate mermaid diagram of the workflow
mermaid_diagram = """
graph TD
    A[intake] --> B[validate]
    B --> C[investigate]
    C --> D[resolve]
    D --> E[close]
    E --> F[END]
"""

# Add visualization to a new HTML file
viz_html = f"""
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: 40px auto; background: #f5f5f5; }}
        .diagram {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <h1>Downside Up Workflow Diagram</h1>
    <div class="diagram">
        <div class="mermaid">
        graph TD
            A[INTAKE] --> B[VALIDATE]
            B --> C[INVESTIGATE]
            C --> D[RESOLVE]
            D --> E[CLOSE]
            E --> F[END]
        </div>
    </div>
</body>
</html>
"""

with open("workflow_diagram.html", "w", encoding="utf-8") as f:
    f.write(viz_html)

print("[DIAGRAM] Open workflow_diagram.html in your browser to see the flow!")

# ============================================================
# CELL 14 - COMPARISON: LangGraph vs LangChain
# ============================================================

comparison = """
LANGGRAPH VS LANGCHAIN - COMPARISON
=====================================

LAB 1 (LangChain) - Creative Agent:
- Freeform problem solving
- Agent decides its own steps
- Unpredictable workflow path
- Good for: open ended tasks, research, exploration

LAB 2 (LangGraph) - Strict Processor:
- Fixed, defined steps
- Workflow path is always the same
- Predictable and traceable
- Good for: compliance, auditing, production systems

WHEN TO USE EACH:
- LangChain: when you want the AI to figure out HOW to solve it
- LangGraph: when YOU define HOW it gets solved, AI just executes each step

TRADE-OFFS:
- LangGraph is more predictable but less flexible
- LangChain is more flexible but harder to audit
- LangGraph is better for regulated industries (finance, healthcare)
- LangChain is better for creative or research tasks
"""

print(comparison)

# Save to file
with open("comparison.txt", "w", encoding="utf-8") as f:
    f.write(comparison)

print("[COMPARISON] Saved to comparison.txt")

# ============================================================
# CELL 15 - FINAL REPORT
# ============================================================

END_TIME = datetime.now()
total_time = END_TIME - START_TIME

report = f"""
# Final Lab Report - NormalObjects LangGraph

## Time
- **Start:** 16:05
- **End:** {END_TIME.strftime('%H:%M')}
- **Total:** {str(total_time).split('.')[0]}

## Time Per Step
| Step | Description | Time |
|------|-------------|------|
| 1 | Setup & State | ~20 min |
| 2 | Workflow Nodes | ~25 min |
| 3 | Build Graph | ~10 min |
| 4 | Test Workflow | ~20 min |
| 5 | Visualize | ~10 min |
| 6 | Comparison | ~10 min |

## Challenges
- Wrong folder in terminal
- .env file not found initially
- Emoji encoding error when writing HTML
- Understanding output options in .py files

## Things to Improve
- Navigate to correct folder before starting
- Use .ipynb during development to save tokens
- Add logging from the beginning

## Things to Learn More About
- LangGraph conditional edges
- LangGraph parallel nodes
- Persisting state to a database
- Converting .ipynb to .py for production
"""

print(report)

with open("final_report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("[REPORT] Saved to final_report.md")