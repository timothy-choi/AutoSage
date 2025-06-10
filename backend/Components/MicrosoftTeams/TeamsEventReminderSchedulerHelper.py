import asyncio
from datetime import datetime
from typing import List, Dict
import aiohttp

scheduled_reminders: List[Dict] = []

async def schedule_event_reminder(webhook_url: str, message: str, remind_at: datetime):
    scheduled_reminders.append({
        "webhook_url": webhook_url,
        "message": message,
        "remind_at": remind_at,
        "sent": False
    })

async def teams_event_reminder_loop():
    while True:
        now = datetime.now()
        for reminder in scheduled_reminders:
            if not reminder["sent"] and now >= reminder["remind_at"]:
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "text": f"⏰ Reminder: {reminder['message']}"
                }
                async with aiohttp.ClientSession() as session:
                    await session.post(reminder["webhook_url"], json=payload)
                reminder["sent"] = True
        await asyncio.sleep(5)