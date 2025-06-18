import aiohttp

async def publish_twitch_clip(broadcaster_id: str, oauth_token: str, client_id: str) -> dict:
    url = "https://api.twitch.tv/helix/clips"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    params = {"broadcaster_id": broadcaster_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=params) as resp:
            if resp.status != 202:
                return {"error": f"Failed to create clip: HTTP {resp.status}", "details": await resp.text()}
            return await resp.json()

async def get_clip_status(clip_id: str, oauth_token: str, client_id: str) -> dict:
    url = f"https://api.twitch.tv/helix/clips?id={clip_id}"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch clip status: HTTP {resp.status}", "details": await resp.text()}
            return await resp.json()