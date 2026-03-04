import threading
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

from apart_agent.graph import build_graph
from apart_agent.notify import notify_n8n

app = Flask(__name__, static_folder="static")
graph = build_graph()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/agent", methods=["POST"])
def run_agent():
    data = request.json
    message = data.get("message", "")
    chat_history = data.get("chat_history", [])  # carry history from frontend

    state = {
        "user_message":      message,
        "retrieved_context": "",
        "agent_response":    "",
        "lead_score":        "",
        "score_reason":      "",
        "actions_taken":     [],
        "chat_history":      chat_history,
        "final_output":      {},
        "language":          data.get("language", ""),
    }

    result = graph.invoke(state)
    output = result["final_output"]

    # HOT leads: notify n8n immediately (Telegram alert)
    if output.get("score") == "HOT":
        threading.Thread(target=notify_n8n, args=(output,), daemon=True).start()

    return jsonify(output)


@app.route("/log-session", methods=["POST"])
def log_session():
    """Called by frontend on CTA click or 3-min inactivity. Logs WARM/COLD sessions."""
    data = request.json
    data["type"] = "inbound"
    threading.Thread(target=notify_n8n, args=(data,), daemon=True).start()
    return jsonify({"status": "logged"})


@app.route("/log-prospect", methods=["POST"])
def log_prospect():
    """Called when Hunter/DuckDuckGo finds outbound contacts."""
    data = request.json
    data["type"] = "outbound"
    threading.Thread(target=notify_n8n, args=(data,), daemon=True).start()
    return jsonify({"status": "logged"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=False)
