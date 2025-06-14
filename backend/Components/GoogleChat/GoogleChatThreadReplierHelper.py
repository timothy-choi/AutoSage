import aiohttp

async def reply_in_google_chat_thread(space_name: str, thread_name: str, access_token: str, message: str) -> dict:
    url = f"https://chat.googleapis.com/v1/{space_name}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": message,
        "thread": {"name": thread_name}
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                return {"status": "replied in thread"}
            return {"error": f"Failed to reply: HTTP {resp.status}"}

async def reply_with_card_in_thread(space_name: str, thread_name: str, access_token: str, title: str, content: str) -> dict:
    url = f"https://chat.googleapis.com/v1/{space_name}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "cardsV2": [
            {
                "cardId": "reply-card",
                "card": {
                    "header": {"title": title},
                    "sections": [
                        {
                            "widgets": [
                                {"textParagraph": {"text": content}}
                            ]
                        }
                    ]
                }
            }
        ],
        "thread": {"name": thread_name}
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                return {"status": "card reply sent"}
            return {"error": f"Failed to send card reply: HTTP {resp.status}"}