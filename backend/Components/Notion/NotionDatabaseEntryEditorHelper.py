import requests
from typing import Dict

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def edit_database_entry(
    notion_token: str,
    page_id: str,
    updated_properties: Dict
) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": updated_properties
    }

    response = requests.patch(f"{NOTION_API_URL}/{page_id}", headers=headers, json=payload)

    return {
        "status": response.status_code,
        "page_id": page_id,
        "updated_properties": updated_properties if response.status_code == 200 else None,
        "error": None if response.status_code == 200 else response.text
    }