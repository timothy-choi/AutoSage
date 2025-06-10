import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import aiohttp

scheduled_meetings: List[Dict] = []

async def schedule_meeting_notification(webhook_url: str, meeting_title: str, start_time: datetime):
    notify_at = start_time - timedelta(minutes=5)  
    scheduled_meetings.append({
        "webhook_url": webhook_url,
        "meeting_title": meeting_title,
        "start_time": start_time,
        "notify_at": notify_at,
        "notified": False
    })

async def teams_meeting_notifier_loop():
    while True:
        now = datetime.utcnow()
        for meeting in scheduled_meetings:
            if not meeting["notified"] and now >= meeting["notify_at"]:
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "text": f"📅 Upcoming Meeting: **{meeting['meeting_title']}** starts in 5 minutes."
                }
                async with aiohttp.ClientSession() as session:
                    await session.post(meeting["webhook_url"], json=payload)
                meeting["notified"] = True
        await asyncio.sleep(5)