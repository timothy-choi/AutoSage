import aiohttp
from typing import List

async def create_twitch_poll(oauth_token: str, client_id: str, broadcaster_id: str, title: str, choices: List[str], duration: int) -> dict:
    url = "https://api.twitch.tv/helix/polls"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    payload = {
        "broadcaster_id": broadcaster_id,
        "title": title,
        "choices": [{"title": choice} for choice in choices],
        "duration": duration
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status in [200, 201]:
                return await resp.json()
            return {"error": f"Failed to create poll: HTTP {resp.status}"}

async def end_twitch_poll(oauth_token: str, client_id: str, poll_id: str, broadcaster_id: str) -> dict:
    url = "https://api.twitch.tv/helix/polls"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    payload = {
        "id": poll_id,
        "broadcaster_id": broadcaster_id,
        "status": "TERMINATED"
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as resp:
            if resp.status in [200, 204]:
                return {"status": "poll ended"}
            return {"error": f"Failed to end poll: HTTP {resp.status}"}

async def get_active_twitch_polls(oauth_token: str, client_id: str, broadcaster_id: str) -> dict:
    url = f"https://api.twitch.tv/helix/polls?broadcaster_id={broadcaster_id}"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to retrieve polls: HTTP {resp.status}"}