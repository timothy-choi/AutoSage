import aiohttp
from datetime import datetime

async def send_access_request(webhook_url: str, requester: str, resource: str, justification: str) -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0072C6",
        "summary": "Access Request",
        "sections": [
            {
                "activityTitle": f"🔐 Access Request from {requester}",
                "text": f"**Resource:** {resource}\n\n**Justification:** {justification}\n\n**Requested At:** {datetime.utcnow().isoformat()}"
            }
        ],
        "potentialAction": [
            {
                "@type": "HttpPOST",
                "name": "Approve",
                "target": "https://your-api-url.com/approve-access"
            },
            {
                "@type": "HttpPOST",
                "name": "Deny",
                "target": "https://your-api-url.com/deny-access"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "access request sent"}
            return {"error": f"Failed to send request: HTTP {resp.status}"}

async def send_bulk_access_requests(webhook_url: str, requests: list[dict]) -> dict:
    results = []
    for req in requests:
        result = await send_access_request(
            webhook_url, req["requester"], req["resource"], req.get("justification", "No justification provided")
        )
        results.append(result)
    return {"results": results}

async def send_access_request_reminder(webhook_url: str, requester: str, resource: str) -> dict:
    message = f"⏰ Reminder: Access request from **{requester}** for **{resource}** is still pending approval."
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FFA500",
        "summary": "Access Request Reminder",
        "sections": [
            {
                "activityTitle": "🔁 Pending Access Reminder",
                "text": message + f"\n\n**Timestamp:** {datetime.utcnow().isoformat()}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "reminder sent"}
            return {"error": f"Failed to send reminder: HTTP {resp.status}"}