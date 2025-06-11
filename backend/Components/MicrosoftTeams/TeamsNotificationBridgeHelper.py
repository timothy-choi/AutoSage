import aiohttp

async def send_teams_notification(webhook_url: str, title: str, message: str, color: str = "0076D7") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [
            {
                "activityTitle": f"**{title}**",
                "text": message
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "sent"}
            return {"error": f"Failed to send notification: HTTP {resp.status}"}

async def send_markdown_notification(webhook_url: str, markdown: str, title: str = "Markdown Update", color: str = "0076D7") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [{"text": markdown}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "sent"}
            return {"error": f"Failed to send markdown notification: HTTP {resp.status}"}

async def send_notification_with_buttons(webhook_url: str, title: str, message: str, buttons: list[dict], color: str = "0076D7") -> dict:
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [{"activityTitle": title, "text": message}],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": btn["label"],
                "targets": [{"os": "default", "uri": btn["url"]}]
            }
            for btn in buttons
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "sent"}
            return {"error": f"Failed to send notification with buttons: HTTP {resp.status}"}

async def send_error_alert(webhook_url: str, error_title: str, error_details: str) -> dict:
    return await send_teams_notification(
        webhook_url=webhook_url,
        title=f"❗ {error_title}",
message=f"```\n{error_details}\n```",
        color="FF0000"
    )

async def send_success_alert(webhook_url: str, title: str, message: str) -> dict:
    return await send_teams_notification(
        webhook_url=webhook_url,
        title=f"✅ {title}",
        message=message,
        color="00C851"
    )