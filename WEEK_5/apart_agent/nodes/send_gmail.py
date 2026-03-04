import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_SENDER       = os.getenv("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_RECIPIENT    = os.getenv("GMAIL_RECIPIENT")


def send_gmail(state):
    if state["lead_score"] != "WARM":
        return state

    if not GMAIL_SENDER or not GMAIL_APP_PASSWORD or not GMAIL_RECIPIENT:
        print("[send_gmail] Skipped — credentials not configured")
        return state

    html = f"""
    <html><body style="font-family:Arial,sans-serif;color:#333;">
      <div style="background:#f0a500;padding:20px;border-radius:8px 8px 0 0;">
        <h1 style="color:white;margin:0;">🌡️ WARM LEAD — Apart Club San Pedro</h1>
      </div>
      <div style="border:1px solid #ddd;padding:24px;border-radius:0 0 8px 8px;">
        <h2 style="color:#555;">Reason</h2>
        <p>{state['score_reason']}</p>
        <h2 style="color:#555;">Their Message</h2>
        <p style="background:#f4f4f4;padding:16px;border-left:4px solid #f0a500;border-radius:4px;">
          {state['user_message']}
        </p>
        <h2 style="color:#555;">Agent Response</h2>
        <p style="background:#f4f4f4;padding:16px;border-left:4px solid #333;border-radius:4px;">
          {state['agent_response']}
        </p>
        <p style="color:#aaa;font-size:11px;margin-top:32px;">
          Sent automatically by the Apart Club AI Agent
        </p>
      </div>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🌡️ WARM Lead — Apart Club San Pedro"
    msg["From"]    = GMAIL_SENDER
    msg["To"]      = GMAIL_RECIPIENT
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_SENDER, GMAIL_RECIPIENT, msg.as_string())
        print("[send_gmail] ✅ Email sent")
        state["actions_taken"].append("gmail_sent")
    except Exception as e:
        print(f"[send_gmail] ❌ {e}")

    return state