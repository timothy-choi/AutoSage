import os
import json
from typing import List, Dict
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)

LOG_FILE = "logs/whatsapp_notifications.jsonl"
os.makedirs("logs", exist_ok=True)


def send_whatsapp_notification(to: str, subject: str, content: str, level: str = "INFO") -> str:
    body = f"🔔 *{subject}* [{level.upper()}]\n\n{content}"
    message = client.messages.create(body=body, from_=from_whatsapp_number, to=to)
    log_notification_event({
        "to": to,
        "subject": subject,
        "content": content,
        "level": level,
        "status": "sent",
        "sid": message.sid,
        "timestamp": datetime.utcnow().isoformat()
    })
    return message.sid


def send_batch_notifications(recipients: List[str], subject: str, content: str) -> List[Dict]:
    results = []
    for to in recipients:
        try:
            sid = send_whatsapp_notification(to, subject, content, level="INFO")
            results.append({"to": to, "status": "sent", "sid": sid})
        except Exception as e:
            log_notification_event({
                "to": to,
                "subject": subject,
                "content": content,
                "level": "INFO",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            results.append({"to": to, "status": "failed", "error": str(e)})
    return results


def log_notification_event(data: dict):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")


def get_notification_history(limit: int = 10) -> List[dict]:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = [json.loads(l) for l in f if l.strip()]
        return lines[-limit:]


def retry_failed_notifications() -> List[str]:
    if not os.path.exists(LOG_FILE):
        return []

    results = []
    with open(LOG_FILE, "r") as f:
        lines = [json.loads(l) for l in f if l.strip()]

    for entry in lines:
        if entry.get("status") == "failed":
            try:
                sid = send_whatsapp_notification(
                    to=entry["to"],
                    subject=entry["subject"],
                    content=entry["content"],
                    level=entry.get("level", "INFO")
                )
                results.append(sid)
            except Exception:
                continue
    return results


def handle_webhook_notification(payload: dict) -> str:
    to = payload.get("to")
    subject = payload.get("subject", "Webhook Alert")
    content = payload.get("content", json.dumps(payload, indent=2))
    return send_whatsapp_notification(to, subject, content, level="WEBHOOK")