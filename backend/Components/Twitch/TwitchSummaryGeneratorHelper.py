import aiohttp
from datetime import timedelta

def format_duration(seconds: int) -> str:
    return str(timedelta(seconds=seconds))

async def generate_twitch_summary(discord_webhook_url: str, streamer_name: str, stream_title: str, viewers: int, clips: list) -> dict:
    summary = f"📊 **Stream Summary for {streamer_name}**\n\n🎯 Title: {stream_title}\n👥 Peak Viewers: {viewers}\n🎞️ Top Clips:"
    for clip in clips:
        summary += f"\n• {clip['title']} ({clip['url']})"
    payload = {"content": summary}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}

async def generate_detailed_summary(discord_webhook_url: str, streamer_name: str, stream_title: str, game: str, duration_seconds: int, viewers: int, followers_gained: int, clips: list) -> dict:
    duration = format_duration(duration_seconds)
    summary = f"📊 **Detailed Summary for {streamer_name}**\n\n🎯 Title: {stream_title}\n🎮 Game: {game}\n⏱️ Duration: {duration}\n👥 Peak Viewers: {viewers}\n📈 Followers Gained: {followers_gained}\n🎞️ Top Clips:"
    for clip in clips:
        summary += f"\n• {clip['title']} ({clip['url']})"
    payload = {"content": summary}
    async with aiohttp.ClientSession() as session:
        async with session.post(discord_webhook_url, json=payload) as resp:
            return {"status": "sent" if resp.status in [200, 204] else f"error {resp.status}"}