import asyncio
from datetime import datetime, timedelta
from typing import List
import aiohttp

reminders: List[dict] = []

async def schedule_twitch_event_reminder(webhook_url: str, event_name: str, remind_at: datetime):
    reminders.append({
        "webhook_url": webhook_url,
        "event_name": event_name,
        "remind_at": remind_at
    })
    return {"status": "reminder scheduled"}

async def twitch_event_reminder_loop():
    while True:
        now = datetime.utcnow()
        due = [r for r in reminders if r["remind_at"] <= now]
        for reminder in due:
            await send_event_reminder(reminder["webhook_url"], reminder["event_name"])
            reminders.remove(reminder)
        await asyncio.sleep(5)

async def send_event_reminder(webhook_url: str, event_name: str):
    payload = {"text": f"⏰ Reminder: **{event_name}** is starting soon!"}
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)