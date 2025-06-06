import requests
from typing import List

def create_slack_poll(token: str, channel: str, question: str, options: List[str]) -> dict:
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Poll:* {question}"}},
        {"type": "actions", "elements": []}
    ]

    for idx, option in enumerate(options):
        blocks[1]["elements"].append({
            "type": "button",
            "text": {"type": "plain_text", "text": option},
            "value": f"poll_option_{idx}",
            "action_id": f"vote_{idx}"
        })

    payload = {
        "channel": channel,
        "blocks": blocks,
        "text": f"Poll: {question}"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    return response.json()