import aiohttp

async def search_hashtag_id(hashtag_name: str, user_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/ig_hashtag_search?user_id={user_id}&q={hashtag_name}&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to search hashtag ID: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data

async def get_hashtag_recent_media(hashtag_id: str, user_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{hashtag_id}/recent_media?user_id={user_id}&fields=id,caption,media_type,media_url,permalink,timestamp&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch recent media: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data