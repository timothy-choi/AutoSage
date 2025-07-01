import requests
from typing import Optional, List, Dict

NOTION_QUERY_API = "https://api.notion.com/v1/databases"
NOTION_VERSION = "2022-06-28"

def query_notion_database(notion_token: str,
                          database_id: str,
                          filter_: Optional[Dict] = None,
                          sorts: Optional[List[Dict]] = None,
                          page_size: Optional[int] = 10) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "page_size": page_size
    }

    if filter_:
        payload["filter"] = filter_
    if sorts:
        payload["sorts"] = sorts

    response = requests.post(f"{NOTION_QUERY_API}/{database_id}/query", headers=headers, json=payload)

    return {
        "status": response.status_code,
        "results": response.json().get("results", []) if response.status_code == 200 else [],
        "error": None if response.status_code == 200 else response.text
    }