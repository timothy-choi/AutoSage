import aiohttp

async def send_crm_update_to_googlechat(crm_data: dict, webhook_url: str) -> dict:
    lead_name = crm_data.get("lead_name")
    status = crm_data.get("status")
    next_step = crm_data.get("next_step", "Not specified")

    message = {
        "text": f"📊 *CRM Update*\n\n*Lead:* {lead_name}\n*Status:* {status}\n*Next Step:* {next_step}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=message) as resp:
            if resp.status != 200:
                return {"error": f"Failed to send to Google Chat: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}

async def send_crm_lead_alert(lead_name: str, webhook_url: str) -> dict:
    message = {
        "text": f"🚨 *New Lead Alert!*\n\n"
                f"A new lead named *{lead_name}* has been added to the CRM."
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=message) as resp:
            if resp.status != 200:
                return {"error": f"Failed to send lead alert: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "success"}

    async def send_crm_followup_reminder(lead_name: str, due_date: str, webhook_url: str) -> dict:
        message = {
            "text": f"⏰ *Follow-up Reminder*\n\n"

                    f"Reminder to follow up with *{lead_name}* by *{due_date}*."
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=message) as resp:
                if resp.status != 200:
                    return {"error": f"Failed to send follow-up reminder: HTTP {resp.status}", "details": await resp.text()}
                return {"status": "success"}