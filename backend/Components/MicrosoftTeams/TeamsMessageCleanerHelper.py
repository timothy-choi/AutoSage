import aiohttp
from datetime import datetime, timedelta

async def delete_teams_message(teams_base_url: str, team_id: str, channel_id: str, message_id: str, access_token: str) -> dict:
    url = f"{teams_base_url}/teams/{team_id}/channels/{channel_id}/messages/{message_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as resp:
            if resp.status == 204:
                return {"status": "deleted"}
            return {"error": f"Failed to delete message: HTTP {resp.status}"}

async def list_channel_messages(teams_base_url: str, team_id: str, channel_id: str, access_token: str) -> list:
    url = f"{teams_base_url}/teams/{team_id}/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("value", [])
            return []

async def bulk_delete_old_messages(teams_base_url: str, team_id: str, channel_id: str, days_old: int, access_token: str) -> dict:
    messages = await list_channel_messages(teams_base_url, team_id, channel_id, access_token)
    cutoff_date = datetime.now() - timedelta(days=days_old)
    deleted = 0
    for msg in messages:
        msg_time = datetime.strptime(msg["createdDateTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if msg_time < cutoff_date:
            await delete_teams_message(teams_base_url, team_id, channel_id, msg["id"], access_token)
            deleted += 1
    return {"deleted_messages": deleted}