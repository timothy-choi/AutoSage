import aiohttp
from datetime import datetime

async def auto_thread_message(webhook_url: str, message: str, thread_context_url: str = None) -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Threaded Message",
        "sections": [
            {
                "text": message
            }
        ]
    }

    if thread_context_url:
        payload["replyToId"] = thread_context_url

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "sent"}
            return {"error": f"Failed to send threaded message: HTTP {resp.status}"}

async def start_new_thread(webhook_url: str, title: str, message: str) -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "text": message
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "thread started"}
            return {"error": f"Failed to start new thread: HTTP {resp.status}"}

async def auto_thread_with_timestamp(webhook_url: str, message: str) -> dict:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    full_message = f"[{timestamp}]\n{message}"
    return await auto_thread_message(webhook_url, full_message)