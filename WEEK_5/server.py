from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from apart_agent.graph import build_graph

app = Flask(__name__)
graph = build_graph()

@app.route("/agent", methods=["POST"])
def run_agent():
    data = request.json
    message = data.get("message", "")
    
    state = {
        "user_message":      message,
        "retrieved_context": "",
        "agent_response":    "",
        "lead_score":        "",
        "score_reason":      "",
        "actions_taken":     [],
        "final_output":      {},
    }
    
    result = graph.invoke(state)
    return jsonify(result["final_output"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=False)
    