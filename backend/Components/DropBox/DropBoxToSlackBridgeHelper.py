import requests

DROPBOX_TEMP_LINK_URL = "https://api.dropboxapi.com/2/files/get_temporary_link"

def get_dropbox_temp_link(access_token: str, file_path: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = { "path": file_path }
    response = requests.post(DROPBOX_TEMP_LINK_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Dropbox temp link error: {response.text}")
    return response.json().get("link")

def send_slack_notification(webhook_url: str, file_name: str, path: str, size: int, preview_url: str = ""):
    message = {
        "text": f":inbox_tray: *New Dropbox File Uploaded*",
        "attachments": [
            {
                "title": file_name,
                "title_link": preview_url,
                "fields": [
                    { "title": "Path", "value": path, "short": True },
                    { "title": "Size", "value": f"{size:,} bytes", "short": True }
                ],
                "color": "#36a64f"
            }
        ]
    }
    res = requests.post(webhook_url, json=message)
    if res.status_code != 200:
        raise Exception(f"Slack webhook error: {res.text}")

def notify_dropbox_file_to_slack(
    dropbox_token: str,
    file_path: str,
    file_name: str,
    file_size: int,
    slack_webhook: str
) -> dict:
    preview_url = get_dropbox_temp_link(dropbox_token, file_path)
    send_slack_notification(slack_webhook, file_name, file_path, file_size, preview_url)
    return {
        "status": "notified",
        "file": file_name,
        "slack_preview_url": preview_url
    }