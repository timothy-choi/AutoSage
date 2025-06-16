import aiohttp

async def announce_twitch_stream(discord_webhook_url: str, streamer_name: str, title: str, game: str, url: str) -> dict:
    content = f"📣 **{streamer_name}** is now live!\n🎮 Game: {game}\n📝 Title: {title}\n🔗 Watch here: {url}"
    payload = {"content": content}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}

async def announce_with_thumbnail(discord_webhook_url: str, streamer_name: str, title: str, game: str, url: str, thumbnail_url: str) -> dict:
    embed = {
        "title": f"{streamer_name} is now live!",
        "description": f"**{title}**\n🎮 {game}\n[Watch here]({url})",
        "image": {"url": thumbnail_url}
    }
    payload = {"embeds": [embed]}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}