import aiohttp

async def send_google_chat_notification(webhook_url: str, text: str) -> dict:
    payload = {"text": text}

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status in [200, 204]:
                return {"status": "notification sent"}
            return {"error": f"Failed to send notification: HTTP {resp.status}"}

async def send_google_chat_card_notification(webhook_url: str, title: str, subtitle: str, content: str) -> dict:
    payload = {
        "cards": [
            {
                "header": {"title": title, "subtitle": subtitle},
                "sections": [
                    {
                        "widgets": [
                            {"textParagraph": {"text": content}}
                        ]
                    }
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status in [200, 204]:
                return {"status": "card notification sent"}
            return {"error": f"Failed to send card: HTTP {resp.status}"}