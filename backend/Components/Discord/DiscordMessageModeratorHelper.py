import requests
import re
from typing import List, Tuple

DISCORD_API = "https://discord.com/api/v10"

BANNED_PATTERNS = [
    r"\bracist\b",
    r"\bhate\b",
    r"\boffensive\b",
    r"\bslur\b",
    r"(?i)\bfake news\b",
    r"(?i)\bn-word\b"
]

def fetch_recent_messages(token: str, channel_id: str, limit: int = 100) -> List[dict]:
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get(
        f"{DISCORD_API}/channels/{channel_id}/messages?limit={limit}",
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def scan_for_violations(messages: List[dict]) -> List[Tuple[dict, List[str]]]:
    flagged = []
    for msg in messages:
        content = msg.get("content", "")
        matched_patterns = [pattern for pattern in BANNED_PATTERNS if re.search(pattern, content)]
        if matched_patterns:
            flagged.append((msg, matched_patterns))
    return flagged

def delete_message(token: str, channel_id: str, message_id: str) -> bool:
    headers = {"Authorization": f"Bot {token}"}
    response = requests.delete(
        f"{DISCORD_API}/channels/{channel_id}/messages/{message_id}",
        headers=headers
    )
    return response.status_code == 204