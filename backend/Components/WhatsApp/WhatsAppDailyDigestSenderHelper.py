import os
import json
from datetime import datetime, timedelta
from typing import List
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)

TRANSCRIPT_FILE = "logs/whatsapp_transcripts.jsonl"

def load_recent_messages(within_hours: int = 24) -> List[dict]:
    if not os.path.exists(TRANSCRIPT_FILE):
        return []

    cutoff = datetime.now() - timedelta(hours=within_hours)
    recent = []
    with open(TRANSCRIPT_FILE, "r") as f:
        for line in f:
            try:
                msg = json.loads(line)
                timestamp = msg.get("timestamp")
                if timestamp:
                    ts = datetime.fromisoformat(timestamp)
                    if ts >= cutoff:
                        recent.append(msg)
            except Exception:
                continue
    return recent

def compile_digest(messages: List[dict]) -> str:
    if not messages:
        return "No WhatsApp activity in the last 24 hours."

    lines = ["📊 *Daily WhatsApp Digest* 📊\n"]
    grouped = {}

    for msg in messages:
        user = msg["from"]
        grouped.setdefault(user, []).append(msg["message_body"])

    for user, msgs in grouped.items():
        lines.append(f"\n👤 *{user}*")
        for m in msgs:
            lines.append(f"• {m}")

    return "\n".join(lines)

def send_digest(to_number: str, digest_text: str) -> str:
    msg = client.messages.create(
        body=digest_text,
        from_=from_whatsapp_number,
        to=to_number
    )
    return msg.sid