import os
import time
import json
import threading
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")  
SEND_API_URL = "https://graph.facebook.com/v17.0/me/messages"

SCHEDULE_LOG_FILE = "logs/facebook_scheduled_messages.jsonl"
os.makedirs("logs", exist_ok=True)

def send_facebook_message_now(recipient_id: str, message: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE"
    }

    response = requests.post(
        SEND_API_URL,
        params={"access_token": PAGE_ACCESS_TOKEN},
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return "sent"
    else:
        raise Exception(f"Facebook API error: {response.status_code} - {response.text}")

def log_scheduled_message(data: dict):
    with open(SCHEDULE_LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def schedule_facebook_message(recipient_id: str, message: str, send_time: str) -> str:
    def delayed_send():
        now = datetime.utcnow()
        target = datetime.fromisoformat(send_time)
        delay = (target - now).total_seconds()
        if delay > 0:
            time.sleep(delay)
        try:
            send_facebook_message_now(recipient_id, message)
        except Exception as e:
            print(f"[Scheduler] Error: {e}")

    log_scheduled_message({
        "recipient_id": recipient_id,
        "message": message,
        "send_time": send_time,
        "status": "scheduled"
    })

    thread = threading.Thread(target=delayed_send)
    thread.start()
    return "scheduled"