import json
import os
from typing import Optional

def parse_whatsapp_webhook(form_data: dict) -> dict:
    return {
        "from": form_data.get("From", ""),
        "to": form_data.get("To", ""),
        "message_body": form_data.get("Body", ""),
        "message_sid": form_data.get("MessageSid", ""),
        "timestamp": form_data.get("Timestamp", ""),
        "profile_name": form_data.get("ProfileName", ""),
        "whatsapp_id": form_data.get("WaId", ""),
        "media_url": form_data.get("MediaUrl0", ""),
        "media_type": form_data.get("MediaContentType0", ""),
        "latitude": form_data.get("Latitude", ""),
        "longitude": form_data.get("Longitude", ""),
        "location_label": form_data.get("Label", "")
    }

def handle_media_messages(data: dict) -> Optional[dict]:
    if data.get("media_url"):
        return {
            "url": data["media_url"],
            "type": data["media_type"]
        }
    return None

def handle_location_messages(data: dict) -> Optional[dict]:
    if data.get("latitude") and data.get("longitude"):
        return {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "label": data.get("location_label", "")
        }
    return None

def auto_reply_to_keywords(message: str) -> Optional[str]:
    responses = {
        "hello": "Hi! How can I assist you today?",
        "help": "Here are some things you can ask me:\n1. Track Order\n2. View Products\n3. Contact Support",
        "thanks": "You're welcome!",
        "bye": "Goodbye! 👋"
    }
    lower_msg = message.strip().lower()
    return responses.get(lower_msg)

def log_incoming_message(data: dict):
    log_entry = json.dumps(data)
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "whatsapp_messages.log"), "a") as f:
        f.write(log_entry + "\n")