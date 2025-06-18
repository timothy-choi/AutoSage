import os
import json
from typing import List

LOG_DIR = "logs"
TRANSCRIPT_FILE = os.path.join(LOG_DIR, "whatsapp_transcripts.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def store_whatsapp_message(message_data: dict):
    with open(TRANSCRIPT_FILE, "a") as f:
        f.write(json.dumps(message_data) + "\n")

def load_all_transcripts() -> List[dict]:
    if not os.path.exists(TRANSCRIPT_FILE):
        return []
    
    with open(TRANSCRIPT_FILE, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def get_transcript_by_user(whatsapp_number: str) -> List[dict]:
    all_messages = load_all_transcripts()
    return [
        msg for msg in all_messages
        if msg.get("from") == whatsapp_number or msg.get("to") == whatsapp_number
    ]