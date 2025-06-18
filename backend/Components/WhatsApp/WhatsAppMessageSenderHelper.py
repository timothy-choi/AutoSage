import os
from datetime import datetime, timedelta
from typing import Optional, List
from twilio.rest import Client
from dotenv import load_dotenv
import threading
import time

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)


def send_whatsapp_message(to_number: str, message: str) -> str:
    msg = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_number
    )
    return msg.sid


def send_whatsapp_media_message(to_number: str, media_url: str, caption: Optional[str] = "") -> str:
    msg = client.messages.create(
        body=caption,
        from_=from_whatsapp_number,
        to=to_number,
        media_url=[media_url]
    )
    return msg.sid


def fetch_whatsapp_message_status(message_sid: str) -> str:
    msg = client.messages(message_sid).fetch()
    return msg.status


def list_recent_whatsapp_messages(limit: int = 10) -> List[dict]:
    messages = client.messages.list(limit=limit)
    return [{
        "sid": m.sid,
        "to": m.to,
        "from": m.from_,
        "body": m.body,
        "status": m.status,
        "date_sent": str(m.date_sent)
    } for m in messages if "whatsapp" in m.from_ or "whatsapp" in m.to]


def schedule_whatsapp_message(to_number: str, message: str, delay_seconds: int) -> str:
    def delayed_send():
        time.sleep(delay_seconds)
        try:
            client.messages.create(
                body=message,
                from_=from_whatsapp_number,
                to=to_number
            )
        except Exception as e:
            print(f"Scheduled message failed: {e}")

    thread = threading.Thread(target=delayed_send)
    thread.start()
    return "scheduled"

def process_incoming_message(from_number: str, message: str) -> str:
    print(f"Received from {from_number}: {message}")
    return f"Echo: {message}"