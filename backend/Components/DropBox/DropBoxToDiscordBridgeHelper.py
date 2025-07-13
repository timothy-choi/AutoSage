import requests

DROPBOX_TEMP_LINK_URL = "https://api.dropboxapi.com/2/files/get_temporary_link"

def get_dropbox_temp_link(access_token: str, file_path: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"path": file_path}
    res = requests.post(DROPBOX_TEMP_LINK_URL, headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Dropbox temp link error: {res.text}")
    return res.json().get("link")

def send_discord_notification(
    discord_webhook_url: str,
    file_name: str,
    file_path: str,
    file_size: int,
    preview_url: str = ""
):
    embed = {
        "title": "New Dropbox File Uploaded",
        "description": f"**{file_name}**",
        "url": preview_url,
        "fields": [
            {"name": "Path", "value": file_path, "inline": True},
            {"name": "Size", "value": f"{file_size:,} bytes", "inline": True}
        ],
        "color": 3066993  
    }
    data = {
        "embeds": [embed]
    }
    res = requests.post(discord_webhook_url, json=data)
    if res.status_code not in (200, 204):
        raise Exception(f"Discord webhook error: {res.text}")

def notify_dropbox_file_to_discord(
    dropbox_token: str,
    file_path: str,
    file_name: str,
    file_size: int,
    discord_webhook_url: str
) -> dict:
    preview_url = get_dropbox_temp_link(dropbox_token, file_path)
    send_discord_notification(discord_webhook_url, file_name, file_path, file_size, preview_url)
    return {
        "status": "notified",
        "file": file_name,
        "discord_preview_url": preview_url
    }