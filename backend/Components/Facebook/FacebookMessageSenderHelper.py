import os
import requests

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

SEND_API_URL = "https://graph.facebook.com/v17.0/me/messages"

def send_facebook_message(recipient_id: str, message_text: str) -> str:
    if not PAGE_ACCESS_TOKEN:
        raise ValueError("FB_PAGE_ACCESS_TOKEN not set")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
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
        raise Exception(f"Facebook Send API error: {response.status_code} - {response.text}")