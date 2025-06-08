import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

scheduled_messages: List[Dict] = []

def schedule_message(channel_id: int, content: str, send_at: datetime):
    scheduled_messages.append({
        "channel_id": channel_id,
        "content": content,
        "send_at": send_at,
        "sent": False
    })

async def scheduler_loop(bot):
    while True:
        now = datetime.utcnow()
        for message in scheduled_messages:
            if not message["sent"] and now >= message["send_at"]:
                channel = bot.get_channel(message["channel_id"])
                if channel:
                    await channel.send(message["content"])
                    message["sent"] = True
        await asyncio.sleep(5)  