import requests
from datetime import datetime, timedelta
from typing import List

DISCORD_API = "https://discord.com/api/v10"

def get_active_threads(token: str, channel_id: str) -> List[dict]:
    url = f"{DISCORD_API}/channels/{channel_id}/threads/active"
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("threads", [])

def archive_thread(token: str, thread_id: str) -> dict:
    url = f"{DISCORD_API}/channels/{thread_id}"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    data = {"archived": True}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def archive_inactive_threads(token: str, channel_id: str, inactive_minutes: int = 60) -> List[str]:
    now = datetime.now()
    threshold = now - timedelta(minutes=inactive_minutes)

    threads = get_active_threads(token, channel_id)
    archived = []

    for thread in threads:
        last_active = datetime.fromisoformat(thread["last_message_timestamp"].replace("Z", "+00:00"))
        if last_active < threshold:
            archive_thread(token, thread["id"])
            archived.append(thread["name"])

    return archived