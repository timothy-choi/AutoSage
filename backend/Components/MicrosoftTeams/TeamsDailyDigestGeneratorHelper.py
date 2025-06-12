import aiohttp
from datetime import datetime

async def send_teams_digest(webhook_url: str, title: str, summary_points: list[str]) -> dict:
    formatted_summary = "\n\n".join(f"- {point}" for point in summary_points)
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": title,
        "sections": [
            {
                "activityTitle": f"📘 {title} - {datetime.utcnow().strftime('%Y-%m-%d')} (UTC)",
                "text": formatted_summary
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "digest sent"}
            return {"error": f"Failed to send digest: HTTP {resp.status}"}

async def send_digest_with_links(webhook_url: str, title: str, summary_links: list[dict]) -> dict:
    formatted_links = "\n\n".join(f"- [{item['text']}]({item['url']})" for item in summary_links)
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "36a64f",
        "summary": title,
        "sections": [
            {
                "activityTitle": f"🔗 {title} - {datetime.utcnow().strftime('%Y-%m-%d')} (UTC)",
                "text": formatted_links
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "digest with links sent"}
            return {"error": f"Failed to send digest with links: HTTP {resp.status}"}

async def send_conditional_digest(webhook_url: str, title: str, data: dict, include_keys: list[str]) -> dict:
    lines = [f"**{key}**: {data[key]}" for key in include_keys if key in data]
    formatted_summary = "\n\n".join(lines)
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF8C00",
        "summary": title,
        "sections": [
            {
                "activityTitle": f"📊 {title} - {datetime.utcnow().strftime('%Y-%m-%d')} (UTC)",
                "text": formatted_summary
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "conditional digest sent"}
            return {"error": f"Failed to send conditional digest: HTTP {resp.status}"}