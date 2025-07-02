import requests
from typing import Dict, List

NOTION_VERSION = "2022-06-28"
PAGE_URL = "https://api.notion.com/v1/pages"
BLOCK_CHILDREN_URL = "https://api.notion.com/v1/blocks/{}/children"

def get_template_blocks(notion_token: str, template_page_id: str) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION
    }

    response = requests.get(BLOCK_CHILDREN_URL.format(template_page_id), headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get template blocks: {response.text}")
    return response.json().get("results", [])

def get_template_properties(notion_token: str, template_page_id: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION
    }

    res = requests.get(f"{PAGE_URL}/{template_page_id}", headers=headers)
    if res.status_code != 200:
        raise Exception(f"Failed to get template properties: {res.text}")
    
    return res.json().get("properties", {})

def apply_template_to_database(notion_token: str, template_page_id: str, database_id: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    properties = get_template_properties(notion_token, template_page_id)
    blocks = get_template_blocks(notion_token, template_page_id)

    payload = {
        "parent": { "database_id": database_id },
        "properties": properties
    }

    page_res = requests.post(PAGE_URL, headers=headers, json=payload)
    if page_res.status_code != 200:
        raise Exception(f"Failed to create new page: {page_res.text}")

    new_page_id = page_res.json()["id"]

    for block in blocks:
        block_payload = {
            "children": [block]
        }
        block_res = requests.patch(BLOCK_CHILDREN_URL.format(new_page_id), headers=headers, json=block_payload)
        if block_res.status_code != 200:
            raise Exception(f"Failed to copy block: {block_res.text}")

    return {
        "status": "success",
        "new_page_id": new_page_id,
        "copied_blocks": len(blocks)
    }