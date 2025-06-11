import aiohttp
import base64

async def fetch_teams_user_info(user_id: str, access_token: str) -> dict:
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return {"error": f"Failed to fetch user info: HTTP {resp.status}"}

async def fetch_user_presence(user_id: str, access_token: str) -> dict:
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/presence"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to fetch presence: HTTP {resp.status}"}

async def fetch_user_photo(user_id: str, access_token: str) -> dict:
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/photo/$value"
    headers = { "Authorization": f"Bearer {access_token}" }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                photo_bytes = await resp.read()
                return {"photo_base64": base64.b64encode(photo_bytes).decode()}
            return {"error": f"Failed to fetch photo: HTTP {resp.status}"}

async def fetch_user_groups(user_id: str, access_token: str) -> dict:
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/memberOf"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                groups = [item.get('displayName') for item in data.get('value', []) if 'displayName' in item]
                return {"groups": groups}
            return {"error": f"Failed to fetch groups: HTTP {resp.status}"}

async def search_users_by_email(email: str, access_token: str) -> dict:
    url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{email}'"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return {"error": f"Failed to search user: HTTP {resp.status}"}