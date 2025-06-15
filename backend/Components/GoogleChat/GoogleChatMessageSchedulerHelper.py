import asyncio
from datetime import datetime, timedelta
import aiohttp

scheduled_messages = []

async def schedule_google_chat_message(webhook_url: str, text: str, send_at: datetime):
    scheduled_messages.append({
        "webhook_url": webhook_url,
        "text": text,
        "send_at": send_at
    })
    return {"status": "scheduled"}

async def schedule_google_chat_card(webhook_url: str, title: str, subtitle: str, content: str, send_at: datetime):
    scheduled_messages.append({
        "webhook_url": webhook_url,
        "card": {
            "title": title,
            "subtitle": subtitle,
            "content": content
        },
        "send_at": send_at
    })
    return {"status": "card scheduled"}

async def google_chat_scheduler_loop():
    while True:
        now = datetime.utcnow()
        to_send = [msg for msg in scheduled_messages if msg["send_at"] <= now]
        for msg in to_send:
            if "card" in msg:
                await send_google_chat_card_notification(
                    msg["webhook_url"],
                    msg["card"]["title"],
                    msg["card"]["subtitle"],
                    msg["card"]["content"]
                )
            else:
                await send_google_chat_notification(msg["webhook_url"], msg["text"])
            scheduled_messages.remove(msg)
        await asyncio.sleep(5)

async def send_google_chat_notification(webhook_url: str, text: str):
    payload = {"text": text}
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)

async def send_google_chat_card_notification(webhook_url: str, title: str, subtitle: str, content: str):
    payload = {
        "cards": [
            {
                "header": {"title": title, "subtitle": subtitle},
                "sections": [
                    {
                        "widgets": [
                            {"textParagraph": {"text": content}}
                        ]
                    }
                ]
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)