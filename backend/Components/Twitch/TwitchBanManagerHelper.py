import aiohttp

async def ban_user(oauth_token: str, client_id: str, broadcaster_id: str, user_id: str, reason: str) -> dict:
    url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={broadcaster_id}"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    payload = {
        "data": {
            "user_id": user_id,
            "reason": reason
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status not in [200, 204]:
                return {"error": f"Failed to ban user: HTTP {resp.status}"}
            return {"status": "User banned"}

async def unban_user(oauth_token: str, client_id: str, broadcaster_id: str, user_id: str) -> dict:
    url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={broadcaster_id}&user_id={user_id}"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as resp:
            if resp.status != 204:
                return {"error": f"Failed to unban user: HTTP {resp.status}"}
            return {"status": "User unbanned"}