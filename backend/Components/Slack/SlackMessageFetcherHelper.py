import requests
from typing import List, Dict

def fetch_slack_messages(token: str, channel: str, limit: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel,
        "limit": limit
    }

    response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Unknown Slack API error"))

    return data.get("messages", [])

def fetch_thread_replies(token: str, channel: str, thread_ts: str) -> List[Dict]:
    response = requests.get(
        "https://slack.com/api/conversations.replies",
        headers={"Authorization": f"Bearer {token}"},
        params={"channel": channel, "ts": thread_ts}
    )
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Failed to fetch thread replies"))
    return data.get("messages", [])

def fetch_user_messages(token: str, channel: str, user_id: str, limit: int = 20) -> List[Dict]:
    messages = fetch_slack_messages(token, channel, limit)
    return [msg for msg in messages if msg.get("user") == user_id]

def search_channel_messages(token: str, channel: str, keyword: str, limit: int = 50) -> List[Dict]:
    messages = fetch_slack_messages(token, channel, limit)
    return [msg for msg in messages if keyword.lower() in msg.get("text", "").lower()]