import aiohttp
from datetime import datetime

async def fetch_user_presence(graph_api_url: str, user_id: str, access_token: str) -> dict:
    url = f"{graph_api_url}/users/{user_id}/presence"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to fetch presence: HTTP {resp.status}"}

async def batch_fetch_presence(graph_api_url: str, user_ids: list[str], access_token: str) -> dict:
    presence_data = {}
    for user_id in user_ids:
        result = await fetch_user_presence(graph_api_url, user_id, access_token)
        presence_data[user_id] = result
    return presence_data

async def fetch_presence_with_timestamp(graph_api_url: str, user_id: str, access_token: str) -> dict:
    presence = await fetch_user_presence(graph_api_url, user_id, access_token)
    presence["timestamp"] = datetime.utcnow().isoformat()
    return presence

async def fetch_filtered_presence(graph_api_url: str, user_ids: list[str], access_token: str, status_filter: list[str]) -> dict:
    results = await batch_fetch_presence(graph_api_url, user_ids, access_token)
    filtered = {uid: data for uid, data in results.items() if data.get("availability") in status_filter}
    return filtered