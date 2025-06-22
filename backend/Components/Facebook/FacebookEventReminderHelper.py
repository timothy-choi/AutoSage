import os
from typing import Dict
import requests
from datetime import datetime, timedelta

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def schedule_event_reminder(post_id: str, message: str, send_at: datetime) -> Dict:
    return {
        "status": "scheduled",
        "post_id": post_id,
        "send_at": send_at.isoformat(),
        "message": message
    }

def send_event_reminder_now(post_id: str, message: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
    res = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "message": message
    })

    if res.status_code == 200:
        return res.json().get("id")
    raise Exception(f"Failed to post reminder: {res.status_code} - {res.text}")