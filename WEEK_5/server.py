import os
import threading
import requests as http
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# Domains to skip — portals, social media, news sites
_SKIP = {
    "wikipedia.org", "facebook.com", "instagram.com", "twitter.com",
    "youtube.com", "linkedin.com", "mercadolibre.com.ar", "zonaprop.com.ar",
    "argenprop.com", "properati.com.ar", "infobae.com", "clarin.com",
    "lanacion.com.ar", "cronista.com", "eldestape.com", "ambito.com",
}


def _search_contacts(query: str) -> list:
    """Search with Tavily and extract {company, domain} from structured results."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query, max_results=8)
        contacts = []
        seen = set()
        for r in response.get("results", []):
            url = r.get("url", "")
            title = r.get("title", "")
            if not url:
                continue
            domain = urlparse(url).netloc.replace("www.", "").strip()
            if not domain or domain in seen:
                continue
            if any(s in domain for s in _SKIP):
                continue
            seen.add(domain)
            company = title.split(" - ")[0].split(" | ")[0].split(" – ")[0].strip()
            if len(company) > 60:
                company = company[:60]
            contacts.append({"company": company, "domain": domain})
        return contacts
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

    contacts = _search_contacts(enhanced_query)
    if contacts is None:
        return jsonify({"error": "Search failed, please try again"}), 500

    # Log ONLY contacts with a domain or email (actionable for outreach)
    for c in contacts:
        if c.get("domain") or c.get("email"):
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
