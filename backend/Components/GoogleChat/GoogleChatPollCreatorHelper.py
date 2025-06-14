import aiohttp
from typing import List

def build_poll_card(question: str, options: List[str]) -> dict:
    buttons = [
        {
            "textButton": {
                "text": option.upper(),
                "onClick": {
                    "openLink": {
                        "url": "https://example.com/submit?poll_option=" + option.replace(" ", "%20")
                    }
                }
            }
        }
        for option in options
    ]

    return {
        "cards": [
            {
                "header": {"title": "Poll", "subtitle": question},
                "sections": [
                    {
                        "widgets": [{"buttons": buttons}]
                    }
                ]
            }
        ]
    }

async def send_google_chat_poll(webhook_url: str, question: str, options: List[str]) -> dict:
    card_payload = build_poll_card(question, options)

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=card_payload) as resp:
            if resp.status == 200:
                return {"status": "poll sent"}
            return {"error": f"Failed to send poll: HTTP {resp.status}"}