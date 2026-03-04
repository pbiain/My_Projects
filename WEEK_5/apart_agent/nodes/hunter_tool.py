import os
import requests
from langchain.tools import tool
from apart_agent.notify import notify_n8n


@tool
def hunter_email_search(company_domain: str) -> str:
    """Find professional email addresses and contacts at a real estate company.
    Use when you have a company name or agency and need to find their contact emails.
    Input must be the company's website domain (e.g., 'remax.com.ar', 'zonaprop.com',
    'coldwellbanker.com.ar'). Do NOT pass a full URL — domain only.
    Returns names, roles, and verified email addresses."""

    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return "HUNTER_API_KEY not set in environment."

    # Strip protocol/path if user passes a full URL
    domain = company_domain.replace("https://", "").replace("http://", "").split("/")[0].strip()

    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": api_key,
        "limit": 5,
        "type": "personal",
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return f"Hunter.io request failed: {e}"

    data = resp.json().get("data", {})
    emails = data.get("emails", [])
    organization = data.get("organization", domain)

    if not emails:
        return f"No email contacts found for {domain}. Try a different domain."

    results = [f"Contacts found at {organization} ({domain}):\n"]
    for e in emails:
        name = f"{e.get('first_name', '')} {e.get('last_name', '')}".strip() or "Unknown"
        position = e.get("position") or "N/A"
        email = e.get("value", "N/A")
        confidence = e.get("confidence", 0)
        results.append(f"- {name} | {position} | {email} (confidence: {confidence}%)")

        # Log each contact to Outbound Prospects sheet (sequential, not background)
        notify_n8n({
            "type":      "outbound",
            "company":   organization,
            "domain":    domain,
            "name":      name,
            "position":  position,
            "email":     email,
            "potential": "HIGH" if confidence >= 70 else "MEDIUM" if confidence >= 40 else "LOW",
        }, background=False)

    return "\n".join(results)
