import aiohttp
from datetime import datetime

async def get_follower_count(instagram_account_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{instagram_account_id}?fields=followers_count&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to retrieve follower count: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return {"follower_count": data.get("followers_count", 0)}

async def get_follower_metric_snapshot(instagram_account_id: str, access_token: str) -> dict:
    snapshot_time = datetime.utcnow().isoformat() + "Z"
    current_stats = await get_follower_count(instagram_account_id, access_token)
    if "error" in current_stats:
        return current_stats
    return {
        "timestamp": snapshot_time,
        "follower_count": current_stats["follower_count"]
    }

async def compare_follower_counts(before_count: int, after_count: int) -> dict:
    change = after_count - before_count
    direction = "increased" if change > 0 else "decreased" if change < 0 else "no change"
    return {
        "before": before_count,
        "after": after_count,
        "change": change,
        "direction": direction
    }