import aiohttp
from typing import List

async def get_engagement_data(instagram_account_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media?fields=id,caption,like_count,comments_count,permalink,timestamp&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch engagement data: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()

    total_likes = 0
    total_comments = 0
    posts_data = []

    for item in data.get("data", []):
        likes = item.get("like_count", 0)
        comments = item.get("comments_count", 0)
        total_likes += likes
        total_comments += comments
        posts_data.append({
            "id": item["id"],
            "caption": item.get("caption"),
            "likes": likes,
            "comments": comments,
            "permalink": item.get("permalink"),
            "timestamp": item.get("timestamp")
        })

    return {
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_posts": len(posts_data),
        "posts": posts_data
    }