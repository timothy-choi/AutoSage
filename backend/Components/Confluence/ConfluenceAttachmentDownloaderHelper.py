import aiohttp
import os

CONFLUENCE_API_BASE = "https://your-domain.atlassian.net/wiki/rest/api"
CONFLUENCE_AUTH_HEADERS = {
    "Authorization": "Basic YOUR_BASE64_ENCODED_AUTH",
    "Accept": "application/json"
}

async def download_confluence_attachment(page_id: str, attachment_filename: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        url = f"{CONFLUENCE_API_BASE}/content/{page_id}/child/attachment"
        async with session.get(url, headers=CONFLUENCE_AUTH_HEADERS) as resp:
            data = await resp.json()
            attachments = data.get("results", [])

            for attachment in attachments:
                if attachment["title"] == attachment_filename:
                    download_link = attachment["_links"]["download"]
                    full_url = f"https://your-domain.atlassian.net{download_link}"

                    async with session.get(full_url, headers=CONFLUENCE_AUTH_HEADERS) as file_resp:
                        if file_resp.status == 200:
                            return await file_resp.read()
                        else:
                            raise Exception(f"Failed to download attachment: {file_resp.status}")

            raise FileNotFoundError(f"Attachment '{attachment_filename}' not found for page {page_id}")