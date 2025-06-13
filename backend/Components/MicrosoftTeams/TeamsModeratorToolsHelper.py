import aiohttp

async def post_warning(webhook_url: str, user: str, reason: str) -> dict:
    message = f"⚠️ Warning issued to **{user}**: {reason}"
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FFA500",
        "summary": "Moderation Warning",
        "sections": [
            {
                "activityTitle": "⚠️ Moderation Alert",
                "text": message
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "warning posted"}
            return {"error": f"Failed to post warning: HTTP {resp.status}"}

async def post_ban_notice(webhook_url: str, user: str, duration: str, reason: str) -> dict:
    message = f"🚫 **{user}** has been banned for {duration}. Reason: {reason}"
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "DC143C",
        "summary": "User Ban Notice",
        "sections": [
            {
                "activityTitle": "🚫 Ban Notification",
                "text": message
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "ban notice posted"}
            return {"error": f"Failed to post ban: HTTP {resp.status}"}