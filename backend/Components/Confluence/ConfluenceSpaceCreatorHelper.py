import aiohttp

CONFLUENCE_API_BASE = "https://your-domain.atlassian.net/wiki/rest/api"
CONFLUENCE_AUTH_HEADERS = {
    "Authorization": "Basic YOUR_BASE64_ENCODED_AUTH",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def create_confluence_space(
    key: str,
    name: str,
    description: str = ""
) -> dict:
    url = f"{CONFLUENCE_API_BASE}/space"

    payload = {
        "key": key.upper(),
        "name": name,
        "description": {
            "plain": {
                "value": description,
                "representation": "plain"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=CONFLUENCE_AUTH_HEADERS, json=payload) as resp:
            if resp.status in [200, 201]:
                return await resp.json()
            else:
                raise Exception(f"Failed to create space: {resp.status} - {await resp.text()}")