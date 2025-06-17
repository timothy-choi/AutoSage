import aiohttp
from typing import List, Dict

async def analyze_trending_hashtags(user_id: str, access_token: str, hashtags: List[str]) -> dict:
    trend_data = []
    async with aiohttp.ClientSession() as session:
        for hashtag in hashtags:
            search_url = f"https://graph.facebook.com/v19.0/ig_hashtag_search?user_id={user_id}&q={hashtag}&access_token={access_token}"
            async with session.get(search_url) as search_resp:
                if search_resp.status != 200:
                    continue
                search_result = await search_resp.json()
                if not search_result.get("data"):
                    continue
                hashtag_id = search_result["data"][0]["id"]

            insights_url = f"https://graph.facebook.com/v19.0/{hashtag_id}/recent_media?user_id={user_id}&fields=id,timestamp&access_token={access_token}"
            async with session.get(insights_url) as insights_resp:
                if insights_resp.status != 200:
                    continue
                recent_data = await insights_resp.json()
                post_count = len(recent_data.get("data", []))
                trend_data.append({"hashtag": hashtag, "recent_posts": post_count})
    return {"trend_data": trend_data}

async def compare_hashtag_trends(trend_data: List[Dict]) -> dict:
    sorted_trends = sorted(trend_data, key=lambda x: x['recent_posts'], reverse=True)
    if not sorted_trends:
        return {"most_trending": None, "least_trending": None, "sorted": []}
    return {
        "most_trending": sorted_trends[0],
        "least_trending": sorted_trends[-1],
        "sorted": sorted_trends
    }