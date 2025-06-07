import requests
from typing import Optional

DISCORD_API = "https://discord.com/api/v10"

def upload_file_to_discord(token: str, channel_id: str, file_path: str, message: Optional[str] = "") -> dict:
    headers = {
        "Authorization": f"Bot {token}"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.split("/")[-1], f, "application/octet-stream")
        }
        data = {
            "content": message
        }
        response = requests.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=headers,
            data=data,
            files=files
        )

    response.raise_for_status()
    return response.json()