import aiohttp

async def send_google_chat_message(webhook_url: str, text: str) -> dict:
    payload = {"text": text}

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "message sent"}
            return {"error": f"Failed to send message: HTTP {resp.status}"}

async def send_google_chat_card(webhook_url: str, title: str, subtitle: str, content: str) -> dict:
    card_payload = {
        "cards": [
            {
                "header": {
                    "title": title,
                    "subtitle": subtitle
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": content
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=card_payload) as resp:
            if resp.status == 200:
                return {"status": "card sent"}
            return {"error": f"Failed to send card: HTTP {resp.status}"}