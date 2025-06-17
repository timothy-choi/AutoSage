import aiohttp

async def forward_instagram_post_to_slack(instagram_post: dict, webhook_url: str) -> dict:
    content = instagram_post.get("caption", "")
    media_url = instagram_post.get("media_url")
    post_url = instagram_post.get("permalink")

    blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📸 *New Instagram Post!*\n\n{content}\n\n🔗 <{post_url}|View Post>"
                }
            }
        ]

    if media_url:
        blocks.append({
            "type": "image",
            "image_url": media_url,
            "alt_text": "Instagram media preview"
        })

    payload = {"blocks": blocks}

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status != 200:
                return {"error": f"Failed to send to Slack: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}
