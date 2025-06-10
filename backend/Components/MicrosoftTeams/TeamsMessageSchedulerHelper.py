import asyncio
from datetime import datetime
from typing import List, Dict
import aiohttp

scheduled_messages: List[Dict] = []

async def schedule_teams_message(webhook_url: str, content: str, send_at: datetime):
    scheduled_messages.append({
        "webhook_url": webhook_url,
        "content": content,
        "send_at": send_at,
        "sent": False
    })

async def teams_message_scheduler_loop():
    while True:
        now = datetime.utcnow()
        for msg in scheduled_messages:
            if not msg["sent"] and now >= msg["send_at"]:
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "text": msg["content"]
                }
                async with aiohttp.ClientSession() as session:
                    await session.post(msg["webhook_url"], json=payload)
                msg["sent"] = True
        await asyncio.sleep(5)