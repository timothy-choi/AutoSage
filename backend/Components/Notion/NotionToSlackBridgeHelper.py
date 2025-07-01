import requests
from typing import Dict

def format_notion_event(event: Dict) -> str:
    title = event.get("title", "Untitled")
    url = event.get("url", "#")
    action = event.get("action", "updated")
    actor = event.get("actor", "Someone")
    return f":notebook: *{actor}* just *{action}* a Notion page: <{url}|{title}>"

def send_to_slack(slack_webhook_url: str, message: str) -> dict:
    response = requests.post(slack_webhook_url, json={"text": message})
    return {
        "status": response.status_code,
        "error": None if response.status_code == 200 else response.text
    }

def bridge_notion_to_slack(slack_webhook_url: str, event: Dict) -> dict:
    message = format_notion_event(event)
    return send_to_slack(slack_webhook_url, message)