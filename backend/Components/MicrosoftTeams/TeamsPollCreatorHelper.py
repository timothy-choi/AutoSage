import aiohttp

async def create_teams_poll(webhook_url: str, question: str, options: list[str]) -> dict:
    if len(options) < 2 or len(options) > 10:
        return {"error": "Poll must have between 2 and 10 options."}

    sections = [{
        "activityTitle": f"📊 **{question}**",
        "facts": [
            {"name": chr(65 + i), "value": opt} for i, opt in enumerate(options)
        ],
        "markdown": True
    }]

    actions = [{
        "@type": "OpenUri",
        "name": f"Vote: {chr(65 + i)}",
        "targets": [{"os": "default", "uri": "https://teams.microsoft.com"}]
    } for i in range(len(options))]

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Poll created",
        "sections": sections,
        "potentialAction": actions
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                return {"status": "Poll sent successfully"}
            return {"error": f"Failed to send poll (HTTP {resp.status})"}