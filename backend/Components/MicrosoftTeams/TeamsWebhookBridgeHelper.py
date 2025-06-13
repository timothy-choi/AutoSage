import aiohttp
from datetime import datetime

async def send_webhook_message(webhook_url: str, title: str, message: str, color: str = "0072C6") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "text": f"{message}\n\n**Sent At:** {datetime.utcnow().isoformat()}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "webhook message sent"}
            return {"error": f"Failed to send webhook message: HTTP {resp.status}"}

async def send_webhook_card(webhook_url: str, title: str, facts: list[dict], color: str = "0072C6") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "facts": facts,
                "markdown": True
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "webhook card sent"}
            return {"error": f"Failed to send webhook card: HTTP {resp.status}"}

async def send_webhook_alert(webhook_url: str, alert_level: str, content: str) -> dict:
    color_map = {
        "info": "0072C6",
        "warning": "FFA500",
        "error": "FF0000"
    }
    color = color_map.get(alert_level.lower(), "0072C6")
    return await send_webhook_message(webhook_url, f"{alert_level.upper()} Alert", content, color)