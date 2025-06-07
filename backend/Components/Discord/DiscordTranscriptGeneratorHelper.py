import requests
from typing import List, Literal

DISCORD_API = "https://discord.com/api/v10"

def fetch_channel_messages(token: str, channel_id: str, limit: int = 100) -> List[dict]:
    headers = {
        "Authorization": f"Bot {token}"
    }
    response = requests.get(
        f"{DISCORD_API}/channels/{channel_id}/messages?limit={limit}",
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def format_transcript(messages: List[dict], format: Literal["text", "json"] = "text") -> str:
    if format == "json":
        import json
        return json.dumps(messages, indent=2)

    lines = []
    for msg in reversed(messages):  
        author = msg["author"]["username"]
        content = msg["content"]
        timestamp = msg["timestamp"]
        lines.append(f"[{timestamp}] {author}: {content}")
    return "\n".join(lines)

def save_transcript_to_file(transcript: str, file_path: str) -> str:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    return file_path