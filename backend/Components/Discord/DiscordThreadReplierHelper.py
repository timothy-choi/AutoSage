import requests
from typing import Optional, List

DISCORD_API = "https://discord.com/api/v10"

def send_plain_reply(token: str, thread_id: str, message: str) -> dict:
    return _send_message(token, thread_id, {"content": message})

def send_markdown_reply(token: str, thread_id: str, message: str, bold=False, italic=False,
                        underline=False, code=False) -> dict:
    if bold:
        message = f"**{message}**"
    if italic:
        message = f"*{message}*"
    if underline:
        message = f"__{message}__"
    if code:
        message = f"`{message}`"
    return _send_message(token, thread_id, {"content": message})

def send_embed_reply(token: str, thread_id: str, title: str, description: str, color: int = 0x5865F2) -> dict:
    embed = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }
    return _send_message(token, thread_id, embed)

def send_mentions_reply(token: str, thread_id: str, message: str, user_ids: Optional[List[str]] = None,
                        role_ids: Optional[List[str]] = None) -> dict:
    mentions = ""
    if user_ids:
        mentions += " ".join([f"<@{uid}>" for uid in user_ids]) + " "
    if role_ids:
        mentions += " ".join([f"<@&{rid}>" for rid in role_ids]) + " "
    return _send_message(token, thread_id, {"content": mentions + message})

def _send_message(token: str, thread_id: str, payload: dict) -> dict:
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{DISCORD_API}/channels/{thread_id}/messages", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()