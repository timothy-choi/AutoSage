import requests
from typing import Optional, List

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def create_notion_page(notion_token: str, database_id: str, title: str, content: Optional[str] = None, tags: Optional[List[str]] = None):
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }

    if tags:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in tags]
        }

    children = []
    if content:
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": content}
                        }
                    ]
                }
            }
        ]

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    if children:
        payload["children"] = children

    response = requests.post(NOTION_API_URL, headers=headers, json=payload)
    return {
        "status": response.status_code,
        "notion_page_url": response.json().get("url") if response.status_code == 200 else None,
        "error": response.text if response.status_code != 200 else None
    }