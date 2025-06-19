import os
import json
from datetime import datetime, timedelta
from typing import List, Dict

TRANSCRIPT_FILE = "logs/whatsapp_transcripts.jsonl"
os.makedirs("logs", exist_ok=True)

def load_messages_for_summary(hours: int = 24) -> List[Dict]:
    if not os.path.exists(TRANSCRIPT_FILE):
        return []

    cutoff = datetime.utcnow() - timedelta(hours=hours)
    messages = []
    
    with open(TRANSCRIPT_FILE, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = entry.get("timestamp")
                if ts:
                    msg_time = datetime.fromisoformat(ts)
                    if msg_time >= cutoff:
                        messages.append(entry)
            except Exception:
                continue
    return messages

def generate_basic_summary(messages: List[Dict]) -> str:
    if not messages:
        return "No activity to summarize."

    users = {}
    for msg in messages:
        sender = msg.get("from")
        if sender not in users:
            users[sender] = []
        users[sender].append(msg.get("message_body", ""))

    summary = ["📋 *Smart Summary of Recent WhatsApp Activity* 📋"]
    for user, msgs in users.items():
        summary.append(f"\n👤 {user} sent {len(msgs)} message(s).")
        preview = " / ".join(msgs[:2])
        if preview:
            summary.append(f"Example: _{preview}_")

    return "\n".join(summary)