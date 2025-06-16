import aiohttp
from typing import List

async def notify_twitch_moderators(webhook_urls: List[str], message: str) -> List[dict]:
    results = []
    for url in webhook_urls:
        payload = {"text": message}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                result = {
                    "url": url,
                    "status": resp.status,
                    "ok": resp.status in [200, 204]
                }
                results.append(result)
    return results

async def notify_with_username(webhook_urls: List[str], username: str, issue: str) -> List[dict]:
    message = f"Moderator Alert: User **{username}** triggered an alert - {issue}"
    return await notify_twitch_moderators(webhook_urls, message)

async def notify_urgent(webhook_urls: List[str], message: str) -> List[dict]:
    urgent_message = f"🚨 URGENT MOD ALERT 🚨\n{message}"
    return await notify_twitch_moderators(webhook_urls, urgent_message)