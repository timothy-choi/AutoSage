import os
import requests
from typing import List, Dict
from datetime import datetime

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def send_facebook_post_notification(page_id: str, message: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{page_id}/feed"
    res = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "message": message
    })

    if res.status_code == 200:
        return res.json()
    raise Exception(f"Post failed: {res.status_code} - {res.text}")

def send_batch_notifications(page_id: str, messages: List[str]) -> List[Dict]:
    results = []
    for msg in messages:
        try:
            result = send_facebook_post_notification(page_id, msg)
            results.append({"message": msg, "status": "sent", "id": result.get("id")})
        except Exception as e:
            results.append({"message": msg, "status": "failed", "error": str(e)})
    return results

def tag_priority_message(message: str) -> str:
    return f"[PRIORITY 🚨] {message}"

def handle_webhook_alert(data: Dict, page_id: str) -> Dict:
    message = data.get("alert_message", "")
    priority = data.get("priority", False)
    if priority:
        message = tag_priority_message(message)
    return send_facebook_post_notification(page_id, message)