import aiohttp

async def forward_twitch_event_to_discord(discord_webhook_url: str, twitch_event: dict) -> dict:
    content = format_twitch_event_as_discord_message(twitch_event)
    payload = {"content": content}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}

def format_twitch_event_as_discord_message(event: dict) -> str:
    event_type = event.get("type", "Unknown")
    username = event.get("user", {}).get("name", "Unknown User")
    description = event.get("description", "No description")
    return f"📢 **Twitch Event**: `{event_type}`\n👤 User: {username}\n📝 {description}"

async def forward_stream_start_to_discord(discord_webhook_url: str, streamer_name: str, stream_title: str, stream_url: str) -> dict:
    content = f"🎥 **{streamer_name}** just went live!\n📌 **{stream_title}**\n🔗 {stream_url}"
    payload = {"content": content}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}

async def forward_clip_to_discord(discord_webhook_url: str, clip_title: str, clip_url: str, creator: str) -> dict:
    content = f"🎞️ New Clip by **{creator}**: **{clip_title}**\n▶️ {clip_url}"
    payload = {"content": content}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}