import requests

def open_dm_channel(token: str, user_id: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"users": user_id}
    response = requests.post("https://slack.com/api/conversations.open", headers=headers, json=payload)
    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Failed to open DM"))

    return data["channel"]["id"]

def send_dm_message(token: str, channel_id: str, message: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel_id,
        "text": message
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    return response.json()