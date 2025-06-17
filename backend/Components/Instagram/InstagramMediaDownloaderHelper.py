import aiohttp

async def download_instagram_media(media_id: str, access_token: str) -> dict:
    metadata_url = f"https://graph.facebook.com/v19.0/{media_id}?fields=id,media_type,media_url,thumbnail_url,timestamp&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(metadata_url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch media metadata: HTTP {resp.status}", "details": await resp.text()}
            metadata = await resp.json()
            return {
                "media_id": metadata.get("id"),
                "media_type": metadata.get("media_type"),
                "media_url": metadata.get("media_url"),
                "thumbnail_url": metadata.get("thumbnail_url"),
                "timestamp": metadata.get("timestamp")
            }

async def get_user_media_list(user_id: str, access_token: str) -> dict:
    media_url = f"https://graph.facebook.com/v19.0/{user_id}/media?fields=id,media_type,media_url,timestamp&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(media_url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch user media: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data

async def get_media_insights(media_id: str, metric: str, access_token: str) -> dict:
    insights_url = f"https://graph.facebook.com/v19.0/{media_id}/insights?metric={metric}&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(insights_url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch media insights: HTTP {resp.status}", "details": await resp.text()}
            insights = await resp.json()
            return insights