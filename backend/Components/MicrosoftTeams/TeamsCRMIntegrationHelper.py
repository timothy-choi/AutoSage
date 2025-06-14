import aiohttp
from typing import Optional

async def create_crm_contact(api_url: str, token: str, name: str, email: str, phone: Optional[str] = None) -> dict:
    payload = {
        "name": name,
        "email": email
    }
    if phone:
        payload["phone"] = phone

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_url}/contacts", json=payload, headers=headers) as resp:
            if resp.status == 201:
                return await resp.json()
            return {"error": f"Failed to create CRM contact: HTTP {resp.status}"}

async def update_crm_contact(api_url: str, token: str, contact_id: str, updates: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(f"{api_url}/contacts/{contact_id}", json=updates, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to update CRM contact: HTTP {resp.status}"}

async def fetch_crm_contact(api_url: str, token: str, contact_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}" 
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_url}/contacts/{contact_id}", headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to fetch CRM contact: HTTP {resp.status}"}