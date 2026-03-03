import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(state):
    if state["lead_score"] != "HOT":
        return state

    message = (
        f"🔥 HOT LEAD ALERT!\n\n"
        f"Message: {state['user_message']}\n"
        f"Reason: {state['score_reason']}\n\n"
        f"Agent response: {state['agent_response'][:300]}..."
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }, timeout=10).raise_for_status()
        print("[send_telegram] ✅ Sent")
    except Exception as e:
        print(f"[send_telegram] ❌ {e}")

    state["actions_taken"].append("telegram_sent")
    return state