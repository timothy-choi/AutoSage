import requests
from typing import Optional, List, Dict

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def create_database_entry(
    notion_token: str,
    database_id: str,
    properties: Dict,
    content_blocks: Optional[List[Dict]] = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    if content_blocks:
        payload["children"] = content_blocks

    response = requests.post(NOTION_API_URL, headers=headers, json=payload)

    return {
        "status": response.status_code,
        "created_page_url": response.json().get("url") if response.status_code == 200 else None,
        "error": None if response.status_code == 200 else response.text
    }