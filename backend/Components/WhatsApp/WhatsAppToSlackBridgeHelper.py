import os
import requests
from datetime import datetime

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  

def format_slack_message(whatsapp_data: dict) -> str:
    from_number = whatsapp_data.get("from", "Unknown")
    profile = whatsapp_data.get("profile_name", "")
    message = whatsapp_data.get("message_body", "")
    time = whatsapp_data.get("timestamp", datetime.utcnow().isoformat())

    return (
        f"*📲 New WhatsApp Message Received*\n"
        f"*From:* {profile or from_number}\n"
        f"*Time:* {time}\n"
        f"*Message:*\n>{message}"
    )

def forward_to_slack(whatsapp_data: dict) -> str:
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL is not set.")

    text = format_slack_message(whatsapp_data)
    response = requests.post(SLACK_WEBHOOK_URL, json={"text": text})

    if response.status_code == 200:
        return "forwarded"
    else:
        raise Exception(f"Failed to send to Slack: {response.status_code} - {response.text}")