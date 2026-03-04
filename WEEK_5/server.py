import os
import threading
import requests as http
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

_ddg = DuckDuckGoSearchRun()

load_dotenv()

from apart_agent.graph import build_graph
from apart_agent.notify import notify_n8n

app = Flask(__name__, static_folder="static")
graph = build_graph()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/outbound")
def outbound():
    return send_from_directory("static", "outbound.html")


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


@app.route("/run-outbound", methods=["POST"])
def run_outbound():
    """DuckDuckGo market search — triggered by outbound UI or n8n schedule."""
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400
    try:
        results = _ddg.run(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"results": results})


@app.route("/find-emails", methods=["POST"])
def find_emails():
    """Hunter.io domain search — returns structured contacts and logs to n8n."""
    data = request.json or {}
    raw = data.get("domain", "")
    domain = raw.replace("https://", "").replace("http://", "").split("/")[0].strip()
    if not domain:
        return jsonify({"error": "domain required"}), 400

    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return jsonify({"error": "HUNTER_API_KEY not configured"}), 500

    try:
        resp = http.get("https://api.hunter.io/v2/domain-search", params={
            "domain": domain, "api_key": api_key, "limit": 5, "type": "personal",
        }, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Hunter.io request failed: {e}"}), 500

    hunter_data = resp.json().get("data", {})
    emails = hunter_data.get("emails", [])
    organization = hunter_data.get("organization", domain)

    if not emails:
        return jsonify({"error": f"No contacts found for {domain}"}), 404

    contacts = []
    for e in emails:
        name = f"{e.get('first_name', '')} {e.get('last_name', '')}".strip() or "Unknown"
        position = e.get("position") or "N/A"
        email_addr = e.get("value", "N/A")
        confidence = e.get("confidence", 0)
        contacts.append({"name": name, "position": position, "email": email_addr, "confidence": confidence})
        threading.Thread(target=notify_n8n, args=({
            "type": "outbound", "company": organization, "domain": domain,
            "name": name, "position": position, "email": email_addr,
            "potential": "HIGH" if confidence >= 70 else "MEDIUM" if confidence >= 40 else "LOW",
        },), daemon=True).start()

    return jsonify({"organization": organization, "domain": domain, "contacts": contacts})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=False)
