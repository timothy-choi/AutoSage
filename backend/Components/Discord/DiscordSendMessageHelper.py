import requests
from typing import Optional, List
import json

DISCORD_API = "https://discord.com/api/v10"

def format_markdown(message: str, bold=False, italic=False, underline=False, code=False) -> str:
    if bold:
        message = f"**{message}**"
    if italic:
        message = f"*{message}*"
    if underline:
        message = f"__{message}__"
    if code:
        message = f"`{message}`"
    return message

def send_discord_message(token: str, channel_id: str, message: str, reply_to: Optional[str] = None,
                         mention_users: Optional[List[str]] = None, mention_roles: Optional[List[str]] = None,
                         markdown: dict = {}, preview: bool = False) -> dict:
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    mentions = ""
    if mention_users:
        mentions += " ".join([f"<@{uid}>" for uid in mention_users]) + " "
    if mention_roles:
        mentions += " ".join([f"<@&{rid}>" for rid in mention_roles]) + " "

    formatted_msg = format_markdown(mentions + message, **markdown)

    payload = {
        "content": formatted_msg
    }

    if reply_to:
        payload["message_reference"] = {"message_id": reply_to}

    if preview:
        return {"preview_payload": payload}

    response = requests.post(f"{DISCORD_API}/channels/{channel_id}/messages", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def send_discord_file(token: str, channel_id: str, file_path: str, message: Optional[str] = "") -> dict:
    headers = {
        "Authorization": f"Bot {token}"
    }
    with open(file_path, "rb") as file_data:
        files = {
            "file": (file_path, file_data, "application/octet-stream")
        }
        data = {"content": message}
        response = requests.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=headers,
            data=data,
            files=files
        )
    response.raise_for_status()
    return response.json()
