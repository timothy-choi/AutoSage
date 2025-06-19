import os
import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  

def format_discord_message(whatsapp_data: dict) -> str:
    from_number = whatsapp_data.get("from", "Unknown")
    profile = whatsapp_data.get("profile_name", "")
    message = whatsapp_data.get("message_body", "")
    time = whatsapp_data.get("timestamp", datetime.utcnow().isoformat())

    return (
        f"📩 **New WhatsApp Message**\n"
        f"👤 **From**: {profile or from_number}\n"
        f"🕒 **Time**: {time}\n"
        f"💬 **Message**:\n{message}"
    )

def forward_to_discord(whatsapp_data: dict) -> str:
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL is not set.")

    content = format_discord_message(whatsapp_data)
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    
    if response.status_code == 204:
        return "forwarded"
    else:
        raise Exception(f"Failed to send to Discord: {response.status_code} - {response.text}")