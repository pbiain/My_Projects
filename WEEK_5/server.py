import os
import json
import threading
import requests as http
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from openai import OpenAI as _OpenAI

_ddg = DuckDuckGoSearchRun()

load_dotenv()

_oai = _OpenAI()  # uses OPENAI_API_KEY from env


def _parse_ddg_contacts(raw: str) -> list:
    """Use GPT-4o-mini to extract structured contacts from DuckDuckGo raw text."""
    try:
        resp = _oai.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": (
                    "Extract real estate company leads from this web search result.\n"
                    "Return ONLY a JSON array. Each object may have these fields (omit fields not found):\n"
                    "  company (string), domain (string), email (string), name (string)\n"
                    "Rules:\n"
                    "- domain must be clean: e.g. remax.com.ar — no http://, no paths\n"
                    "- Include ONLY entries that have at least one of: domain, email, or company\n"
                    "- Skip generic articles, FAQs, blog posts, or entries with no contact info\n"
                    "- If same company appears multiple times, merge into one entry\n"
                    "- Return [] if nothing useful found\n\n"
                    f"Search results:\n{raw}\n\n"
                    "Return valid JSON array only, no explanation."
                ),
            }],
        )
        parsed = json.loads(resp.choices[0].message.content)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []

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
    """DuckDuckGo market search — parses results into structured contacts."""
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400

    # Auto-enhance with location context
    location_terms = ["san pedro", "argentina", "buenos aires"]
    if not any(t in query.lower() for t in location_terms):
        enhanced_query = f"{query} san pedro buenos aires argentina"
    else:
        enhanced_query = query

    try:
        raw = _ddg.run(enhanced_query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Parse raw text into structured contacts via GPT
    contacts = _parse_ddg_contacts(raw)

    # Log ONLY contacts with actionable data (domain, email, or company)
    for c in contacts:
        if any(c.get(f) for f in ["domain", "email", "company"]):
            threading.Thread(target=notify_n8n, args=({
                "type":     "outbound",
                "company":  c.get("company", "—"),
                "domain":   c.get("domain", "—"),
                "name":     c.get("name", "—"),
                "position": "—",
                "email":    c.get("email", "—"),
                "potential": "MEDIUM",
            },), daemon=True).start()

    return jsonify({"contacts": contacts, "query_used": enhanced_query})


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
        # Log the attempt even with no results
        threading.Thread(target=notify_n8n, args=({
            "type": "outbound", "company": organization, "domain": domain,
            "name": "—", "position": "—", "email": "—", "potential": "NOT FOUND",
        },), daemon=True).start()
        return jsonify({"error": f"No contacts found for {domain}. Hunter.io has limited coverage of Argentine local companies — try larger domains like remax.com.ar or zonaprop.com.ar"}), 404

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
