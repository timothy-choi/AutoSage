import aiohttp

CONFLUENCE_API_BASE = "https://your-domain.atlassian.net/wiki/rest/api"
CONFLUENCE_AUTH_HEADERS = {
    "Authorization": "Basic YOUR_BASE64_ENCODED_AUTH",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def add_inline_comment(page_id: str, comment_text: str, anchored_content_id: str) -> dict:
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
        },
        "metadata": {
            "annotation": {
                "prefix": "inline-comment",
                "type": "inline",
                "attributes": {
                    "target": {
                        "id": anchored_content_id,
                        "type": "content"
                    }
                }
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=CONFLUENCE_AUTH_HEADERS, json=payload) as resp:
            if resp.status in (200, 201):
                return await resp.json()
            else:
                raise Exception(f"Failed to add inline comment: {resp.status} {await resp.text()}")