import aiohttp

async def send_twitch_chat_message(oauth_token: str, client_id: str, broadcaster_id: str, message: str) -> dict:
    url = f"https://api.twitch.tv/helix/chat/messages"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    payload = {
        "broadcaster_id": broadcaster_id,
        "message": message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status in [200, 202, 204]:
                return {"status": "message sent"}
            return {"error": f"Failed to send message: HTTP {resp.status}"}

async def send_twitch_whisper(oauth_token: str, client_id: str, from_user_id: str, to_user_id: str, message: str) -> dict:
    url = f"https://api.twitch.tv/helix/whispers?from_user_id={from_user_id}&to_user_id={to_user_id}"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    payload = {"message": message}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 204:
                return {"status": "whisper sent"}
            return {"error": f"Failed to send whisper: HTTP {resp.status}"}