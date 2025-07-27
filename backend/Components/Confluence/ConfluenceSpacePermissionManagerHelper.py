import aiohttp
from config import CONFLUENCE_API_BASE, CONFLUENCE_AUTH_HEADERS

async def set_space_permissions(space_key: str, permissions: list) -> dict:
    url = f"{CONFLUENCE_API_BASE}/space/{space_key}/permission"
    payload = {"permissions": permissions}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=CONFLUENCE_AUTH_HEADERS, json=payload) as resp:
            if resp.status in [200, 201]:
                return await resp.json()
            else:
                raise Exception(f"Failed to set permissions: {resp.status} - {await resp.text()}")

async def list_space_permissions(space_key: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/space/{space_key}/permission"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=CONFLUENCE_AUTH_HEADERS) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"Failed to list permissions: {resp.status} - {await resp.text()}")

async def remove_space_permission(space_key: str, permission_id: int) -> dict:
    url = f"{CONFLUENCE_API_BASE}/space/{space_key}/permission/{permission_id}"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=CONFLUENCE_AUTH_HEADERS) as resp:
            if resp.status in [200, 204]:
                return {"removed": True}
            else:
                raise Exception(f"Failed to delete permission: {resp.status} - {await resp.text()}")

async def check_user_permission(space_key: str, user_account_id: str, permission_key: str) -> bool:
    permissions = await list_space_permissions(space_key)
    for perm in permissions.get("results", []):
        if (
            perm.get("operation", {}).get("key") == permission_key and
            perm.get("subjects", {}).get("user", {}).get("accountId") == user_account_id
        ):
            return True
    return False