import asyncio
from datetime import datetime

scheduled_reminders = []

async def schedule_event_reminder(bot, channel_id: int, message: str, remind_at: datetime):
    scheduled_reminders.append({
        "channel_id": channel_id,
        "message": message,
        "remind_at": remind_at,
        "sent": False
    })

async def event_reminder_loop(bot):
    while True:
        now = datetime.utcnow()
        for reminder in scheduled_reminders:
            if not reminder["sent"] and now >= reminder["remind_at"]:
                channel = bot.get_channel(reminder["channel_id"])
                if channel:
                    await channel.send(f"⏰ Reminder: {reminder['message']}")
                    reminder["sent"] = True
        await asyncio.sleep(10)