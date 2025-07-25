import aiohttp

CONFLUENCE_API_BASE = "https://your-domain.atlassian.net/wiki/rest/api"
CONFLUENCE_AUTH_HEADERS = {
    "Authorization": "Basic YOUR_BASE64_ENCODED_AUTH",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def add_confluence_comment(page_id: str, comment_text: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/content/"

    payload = {
        "type": "comment",
        "container": {
            "type": "page",
            "id": page_id
        },
        "body": {
            "storage": {
                "value": comment_text,
                "representation": "storage"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=CONFLUENCE_AUTH_HEADERS, json=payload) as resp:
            if resp.status == 200 or resp.status == 201:
                return await resp.json()
            else:
                raise Exception(f"Failed to add comment: {resp.status} {await resp.text()}")