import requests
import json
from config import SLACK_WEBHOOK_URL

def format_confluence_update(update_type: str, page_title: str, page_url: str, author: str, comment: str = "") -> str:
    emoji_map = {
        "created": ":new:",
        "updated": ":pencil2:",
        "commented": ":speech_balloon:",
    }

    emoji = emoji_map.get(update_type, ":page_facing_up:")
    message = f"{emoji} *{author}* {update_type} a page: *<{page_url}|{page_title}>*"

    if comment:
        message += f"\n>_{comment}_"

    return message

def send_to_slack(message: str) -> dict:
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(SLACK_WEBHOOK_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return {"success": True, "message": "Sent to Slack"}
    else:
        return {"success": False, "message": "Failed to send", "details": response.text}

def bridge_confluence_to_slack(update_type: str, page_title: str, page_url: str, author: str, comment: str = "") -> dict:
    slack_msg = format_confluence_update(update_type, page_title, page_url, author, comment)
    return send_to_slack(slack_msg)