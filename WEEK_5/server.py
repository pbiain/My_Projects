import os
import threading
import requests as http
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# Domains to skip — only social media and encyclopedias
_SKIP = {
    "wikipedia.org", "facebook.com", "instagram.com", "twitter.com",
    "youtube.com", "linkedin.com", "reddit.com", "tiktok.com",
}


def _search_contacts(query: str):
    """Search with Tavily and extract {company, domain} from structured results.
    Returns (contacts_list, error_string) — error is None on success."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return [], "TAVILY_API_KEY not set in environment"
    try:
        client = TavilyClient(api_key=api_key)
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
        return contacts, None
    except Exception as e:
        return [], str(e)

from apart_agent.graph import build_graph
from apart_agent.notify import notify_n8n
from apart_agent.nodes.classify_lead import classify_lead
from apart_agent.nodes.send_telegram import send_telegram
from apart_agent.nodes.send_gmail import send_gmail

app = Flask(__name__, static_folder="static")
graph = build_graph()

# Strong buying intent — classify sync so CTA button appears in response
STRONG_HOT_KEYWORDS = {
    "comprar", "interesado", "me interesa", "quiero", "quisiera", "lo compro",
    "llamar", "llamame", "llámame", "agente", "asesor", "contactar", "contacto",
    "teléfono", "telefono", "whatsapp", "hablar", "habla",
    "buy", "interested", "i want", "i'd like to buy", "i'll take", "purchase",
    "agent", "call", "phone", "talk", "speak", "contact", "advisor", "reach",
}

# Softer signals — classify async (no CTA needed, just logging/notifications)
SOFT_KEYWORDS = {
    "precio", "lote", "visitar", "pago", "cuota", "financ",
    "price", "lot", "visit", "invest", "payment", "budget",
}


def classify_and_notify(state):
    """Runs in a background thread — classifies the lead and sends notifications.

    HOT  → Telegram alert to owner + log to Google Sheets
           Criteria: specific budget, payment plan intent, mentions ROI, ready to buy
    WARM → Gmail notification to owner + log to Google Sheets
           Criteria: asking about prices/availability, building regs, general interest
    COLD → no action, no logging (session end handled by /log-session if score warrants it)
    """
    try:
        state = classify_lead(state)
        score = state["lead_score"]
        output = state.get("final_output", {})
        output["score"] = score
        output["score_reason"] = state.get("score_reason", "")
        if score == "HOT":
            send_telegram(state)
            notify_n8n(output)          # HOT: Telegram + Google Sheets log
        elif score == "WARM":
            send_gmail(state)
            notify_n8n(output)          # WARM: Gmail + Google Sheets log
        # COLD: no notification, no Sheets log
    except Exception:
        pass


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
    chat_history = data.get("chat_history", [])

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

    msg_lower = message.lower()
    is_strong_hot = any(kw in msg_lower for kw in STRONG_HOT_KEYWORDS)
    is_soft       = any(kw in msg_lower for kw in SOFT_KEYWORDS)

    if is_strong_hot:
        # Sync: need the score NOW so the CTA button can appear in the response
        # HOT → Telegram + Sheets | WARM → Gmail + Sheets | COLD → no action
        state["final_output"] = output
        state = classify_lead(state)
        output["score"] = state["lead_score"]
        output["score_reason"] = state["score_reason"]
        def _notify_sync(s, o):
            score = s["lead_score"]
            if score == "HOT":
                send_telegram(s)
                notify_n8n(o)           # HOT: Telegram + Google Sheets log
            elif score == "WARM":
                send_gmail(s)
                notify_n8n(o)           # WARM: Gmail + Google Sheets log
            # COLD: no notification, no Sheets log
        threading.Thread(target=_notify_sync, args=(state, output), daemon=True).start()
    elif is_soft:
        # Async: buying signal detected — classify + notify in background
        # HOT/WARM logged to Sheets; COLD silently dropped (see classify_and_notify)
        state["final_output"] = output
        threading.Thread(target=classify_and_notify, args=(state,), daemon=True).start()

    return jsonify(output)


@app.route("/log-session", methods=["POST"])
def log_session():
    """Called by frontend on CTA click or 3-min inactivity.
    HOT/WARM: logged to Google Sheets
    COLD: silently dropped — no value in logging uninterested sessions
    """
    data = request.json
    score = data.get("score", "COLD")
    if score not in ("HOT", "WARM"):
        return jsonify({"status": "skipped"})
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

    contacts, err = _search_contacts(enhanced_query)
    if err:
        return jsonify({"error": f"Search error: {err}"}), 500

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
        phone = e.get("phone_number", "") or ""
        contacts.append({"name": name, "position": position, "email": email_addr, "confidence": confidence, "phone": phone})
        threading.Thread(target=notify_n8n, args=({
            "type": "outbound", "company": organization, "domain": domain,
            "name": name, "position": position, "email": email_addr,
            "potential": "HIGH" if confidence >= 70 else "MEDIUM" if confidence >= 40 else "LOW",
        },), daemon=True).start()

    return jsonify({"organization": organization, "domain": domain, "contacts": contacts})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=False)
