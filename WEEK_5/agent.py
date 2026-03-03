import sys
import json
import os
from dotenv import load_dotenv

load_dotenv()

from apart_agent.graph import build_graph

def run_agent(user_message: str) -> dict:
    graph = build_graph()
    state = {
        "user_message":      user_message,
        "retrieved_context": "",
        "agent_response":    "",
        "lead_score":        "",
        "score_reason":      "",
        "actions_taken":     [],
        "final_output":      {},
    }
    result = graph.invoke(state)
    return result["final_output"]

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Hola, quiero información"
    output = run_agent(message)
    print(json.dumps(output, ensure_ascii=False, indent=2))