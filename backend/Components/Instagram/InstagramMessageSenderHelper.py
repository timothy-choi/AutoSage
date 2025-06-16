import aiohttp

async def send_instagram_dm(recipient_id: str, message: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{recipient_id}/messages"
    payload = {
        "messaging_type": "UPDATE",
        "message": {"text": message},
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status not in [200, 201]:
                return {"error": f"Failed to send message: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "message sent", "recipient_id": recipient_id}

async def send_instagram_media_dm(recipient_id: str, media_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{recipient_id}/messages"
    payload = {
        "messaging_type": "UPDATE",
        "message": {"attachment": {"type": "image", "payload": {"attachment_id": media_id}}},
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status not in [200, 201]:
                return {"error": f"Failed to send media: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "media sent", "recipient_id": recipient_id}

async def mark_dm_as_seen(recipient_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{recipient_id}/messages"
    payload = {
        "sender_action": "mark_seen",
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status not in [200, 201]:
                return {"error": f"Failed to mark as seen: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "marked as seen", "recipient_id": recipient_id}