import aiohttp

async def sync_instagram_post_to_twitter(instagram_post: dict, bearer_token: str) -> dict:
    tweet_text = instagram_post.get("caption", "")
    post_url = instagram_post.get("permalink")
    media_url = instagram_post.get("media_url")

    text = f"📸 {tweet_text}\n{post_url}"
    tweet_endpoint = "https://api.twitter.com/2/tweets"

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}

    async with aiohttp.ClientSession() as session:
        async with session.post(tweet_endpoint, headers=headers, json=payload) as resp:
            if resp.status != 201:
                return {"error": f"Failed to sync with Twitter: HTTP {resp.status}", "details": await resp.text()}
            return await resp.json()