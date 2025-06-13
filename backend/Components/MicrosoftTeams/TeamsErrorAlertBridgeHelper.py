import aiohttp
from datetime import datetime

async def send_error_alert(webhook_url: str, error_message: str, service_name: str = "Unknown Service") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000",
        "summary": f"Error Alert from {service_name}",
        "sections": [
            {
                "activityTitle": f"🚨 Error in {service_name}",
                "text": f"**Timestamp:** {datetime.utcnow().isoformat()}\n\n**Error:** {error_message}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "alert sent"}
            return {"error": f"Failed to send alert: HTTP {resp.status}"}

async def send_critical_alert(webhook_url: str, message: str, system_name: str) -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "8B0000",
        "summary": f"Critical Alert - {system_name}",
        "sections": [
            {
                "activityTitle": f"❗ CRITICAL: {system_name}",
                "text": f"{message}\n\n**Timestamp:** {datetime.utcnow().isoformat()}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "critical alert sent"}
            return {"error": f"Failed to send critical alert: HTTP {resp.status}"}

async def send_warning_alert(webhook_url: str, message: str, service_name: str) -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FFA500",
        "summary": f"Warning Alert - {service_name}",
        "sections": [
            {
                "activityTitle": f"⚠️ Warning: {service_name}",
                "text": f"{message}\n\n**Timestamp:** {datetime.utcnow().isoformat()}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "warning alert sent"}
            return {"error": f"Failed to send warning alert: HTTP {resp.status}"}