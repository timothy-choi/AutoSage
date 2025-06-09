import requests
from typing import Optional

GRAPH_API = "https://graph.microsoft.com/v1.0"


def send_teams_message(access_token: str, team_id: str, channel_id: str, message: str) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "body": {
            "content": message
        }
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def send_markdown_message(access_token: str, team_id: str, channel_id: str, markdown: str) -> dict:
    return send_teams_message(access_token, team_id, channel_id, markdown)


def reply_to_channel_message(access_token: str, team_id: str, channel_id: str, parent_message_id: str, reply_text: str) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages/{parent_message_id}/replies"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "body": {
            "content": reply_text
        }
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def send_mention_message(access_token: str, team_id: str, channel_id: str, user_id: str, display_name: str, message: str) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages"
    body = {
        "body": {
            "contentType": "html",
            "content": f'<at id="0">{display_name}</at> {message}'
        },
        "mentions": [
            {
                "id": 0,
                "mentionText": display_name,
                "mentioned": {
                    "user": {
                        "id": user_id,
                        "displayName": display_name
                    }
                }
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def schedule_teams_message(task_queue, delay_seconds: int, access_token: str, team_id: str, channel_id: str, message: str):
    task_queue.apply_async(
        func=send_teams_message,
        args=(access_token, team_id, channel_id, message),
        countdown=delay_seconds
    )
    return {"scheduled": True, "delay_seconds": delay_seconds}


def send_adaptive_card(access_token: str, team_id: str, channel_id: str, card_json: dict) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages"
    body = {
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_json
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()