import requests

def post_slack_message(token: str, channel: str, message: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": message
    }

    response = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    return response.json()