import aiohttp

async def forward_instagram_post_to_discord(instagram_post: dict, webhook_url: str) -> dict:
    content = instagram_post.get("caption", "")
    media_url = instagram_post.get("media_url")
    post_url = instagram_post.get("permalink")

    payload = {
        "content": f"📸 **New Instagram Post!**\n{content}\n🔗 {post_url}"
    }

    if media_url:
        payload["embeds"] = [{
            "image": {"url": media_url}
        }]

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status != 204:
                return {"error": f"Failed to send to Discord: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}

async def forward_instagram_story_to_discord(story_url: str, webhook_url: str) -> dict:
    payload = {
        "content": f"📖 **New Instagram Story!**\n🔗 {story_url}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status != 204:
                return {"error": f"Failed to send story to Discord: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}

async def forward_instagram_reel_to_discord(reel_url: str, caption: str, webhook_url: str) -> dict:
    payload = {
        "content": f"🎬 **New Instagram Reel!**\n{caption}\n🔗 {reel_url}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status != 204:
                return {"error": f"Failed to send reel to Discord: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}