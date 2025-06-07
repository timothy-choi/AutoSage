import requests
from typing import Optional, List

DISCORD_API = "https://discord.com/api/v10"

def send_discord_message(token: str, channel_id: str, message: str, reply_to: Optional[str] = None,
                         mention_users: Optional[List[str]] = None, mention_roles: Optional[List[str]] = None) -> dict:
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    mentions = ""
    if mention_users:
        mentions += " ".join([f"<@{uid}>" for uid in mention_users]) + " "
    if mention_roles:
        mentions += " ".join([f"<@&{rid}>" for rid in mention_roles]) + " "

    payload = {
        "content": mentions + message,
    }

    if reply_to:
        payload["message_reference"] = {"message_id": reply_to}

    url = f"{DISCORD_API}/channels/{channel_id}/messages"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def send_embed(token: str, channel_id: str, title: str, description: str, color: int = 0x5865F2) -> dict:
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }

    url = f"{DISCORD_API}/channels/{channel_id}/messages"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()