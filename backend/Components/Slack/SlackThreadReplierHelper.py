import requests

def reply_to_slack_thread(token: str, channel: str, thread_ts: str, message: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": channel,
        "text": message,
        "thread_ts": thread_ts
    }

    response = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    return response.json()

def upload_slack_file(token: str, channels: str, file_path: str, title: str = "") -> dict:
    """Uploads a file to Slack in a specific channel/thread."""
    with open(file_path, "rb") as file_content:
        files = {'file': file_content}
        data = {
            "channels": channels,
            "title": title
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post("https://slack.com/api/files.upload", headers=headers, data=data, files=files)
        return response.json()