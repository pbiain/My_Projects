import os
import threading
import requests

_N8N_URL = None


def _get_url():
    global _N8N_URL
    if _N8N_URL is None:
        _N8N_URL = os.getenv("N8N_WEBHOOK_URL", "")
    return _N8N_URL


def notify_n8n(payload: dict, background: bool = True):
    """POST payload to n8n webhook. Runs in background thread by default."""
    url = _get_url()
    if not url:
        return

    def _send():
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception:
            pass

    if background:
        threading.Thread(target=_send, daemon=True).start()
    else:
        _send()
