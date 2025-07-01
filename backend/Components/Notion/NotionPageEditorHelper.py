import requests
from typing import Optional, List

NOTION_PAGE_URL = "https://api.notion.com/v1/pages"
NOTION_BLOCKS_URL = "https://api.notion.com/v1/blocks"
NOTION_VERSION = "2022-06-28"

def update_notion_page_properties(notion_token: str, page_id: str, title: Optional[str], tags: Optional[List[str]]):
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    properties = {}
    if title:
        properties["Name"] = {
            "title": [
                {
                    "text": {"content": title}
                }
            ]
        }
    if tags:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in tags]
        }

    if not properties:
        return {"status": "skipped", "message": "No properties to update"}

    response = requests.patch(f"{NOTION_PAGE_URL}/{page_id}", headers=headers, json={"properties": properties})
    return {
        "status": response.status_code,
        "updated_properties": properties,
        "error": response.text if response.status_code != 200 else None
    }

def update_notion_page_content(notion_token: str, page_id: str, content: Optional[str]):
    if not content:
        return {"status": "skipped", "message": "No content to update"}

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    block = {
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

    response = requests.patch(
        f"{NOTION_BLOCKS_URL}/{page_id}/children",
        headers=headers,
        json={"children": [block]}
    )

    return {
        "status": response.status_code,
        "content": content,
        "error": response.text if response.status_code != 200 else None
    }

def edit_notion_page(notion_token: str, page_id: str, title: Optional[str], tags: Optional[List[str]], content: Optional[str]):
    prop_result = update_notion_page_properties(notion_token, page_id, title, tags)
    content_result = update_notion_page_content(notion_token, page_id, content)
    return {
        "property_update": prop_result,
        "content_update": content_result
    }