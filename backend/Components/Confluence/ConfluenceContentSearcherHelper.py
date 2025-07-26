import aiohttp

CONFLUENCE_API_BASE = "https://your-domain.atlassian.net/wiki/rest/api"
CONFLUENCE_AUTH_HEADERS = {
    "Authorization": "Basic YOUR_BASE64_ENCODED_AUTH",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def search_confluence_content(
    title: str = None,
    label: str = None,
    content_type: str = "page",
    cql: str = None,
    limit: int = 10
) -> dict:
    if cql:
        query = cql
    else:
        parts = [f"type={content_type}"]
        if title:
            parts.append(f'title~"{title}"')
        if label:
            parts.append(f'label="{label}"')
        query = " AND ".join(parts)

    url = f"{CONFLUENCE_API_BASE}/content/search?cql={query}&limit={limit}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=CONFLUENCE_AUTH_HEADERS) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"Search failed: {resp.status} - {await resp.text()}")