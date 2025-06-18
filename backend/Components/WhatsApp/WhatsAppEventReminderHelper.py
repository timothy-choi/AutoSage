import os
import json
import threading
import time
from datetime import datetime
from typing import List
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)

REMINDER_LOG_FILE = "logs/whatsapp_event_reminders.jsonl"
os.makedirs("logs", exist_ok=True)


def save_reminder_to_log(reminder: dict):
    with open(REMINDER_LOG_FILE, "a") as f:
        f.write(json.dumps(reminder) + "\n")


def send_whatsapp_reminder(to: str, message: str) -> str:
    msg = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to
    )
    return msg.sid


def schedule_reminder(to: str, message: str, event_time: str) -> str:
    def wait_and_send():
        now = datetime.utcnow()
        send_at = datetime.fromisoformat(event_time)
        delay = (send_at - now).total_seconds()

        if delay > 0:
            time.sleep(delay)

        try:
            send_whatsapp_reminder(to, message)
        except Exception as e:
            print(f"[Reminder] Failed to send: {e}")

    reminder_data = {
        "to": to,
        "message": message,
        "event_time": event_time
    }

    save_reminder_to_log(reminder_data)
    thread = threading.Thread(target=wait_and_send)
    thread.start()

    return "scheduled"