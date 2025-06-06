import requests
from typing import List

def fetch_recent_messages(token: str, channel: str, limit: int = 20) -> List[str]:
    headers = {"Authorization": f"Bearer {token}"}
    params = {"channel": channel, "limit": limit}
    response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
    messages = response.json().get("messages", [])
    return [msg.get("text", "") for msg in messages if "text" in msg]


def summarize_text(text: str) -> str:
    lines = text.split('\n')
    important_lines = [line for line in lines if any(word in line.lower() for word in ["deadline", "update", "next", "plan", "issue"])]
    if not important_lines:
        return "Summary: No important updates found."
    return "Summary:\n" + "\n".join(important_lines[:5])


def fetch_and_summarize(token: str, channel: str, limit: int = 20) -> str:
    messages = fetch_recent_messages(token, channel, limit)
    full_text = "\n".join(messages)
    return summarize_text(full_text)