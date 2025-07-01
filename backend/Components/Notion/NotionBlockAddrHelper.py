import requests
from typing import List, Literal

NOTION_BLOCKS_API = "https://api.notion.com/v1/blocks"
NOTION_VERSION = "2022-06-28"

def build_block(block_type: Literal["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"], content: str):
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": content}
                }
            ]
        }
    }

def add_blocks_to_notion_page(notion_token: str, page_id: str, blocks: List[dict]):
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    response = requests.patch(
        f"{NOTION_BLOCKS_API}/{page_id}/children",
        headers=headers,
        json={"children": blocks}
    )

    return {
        "status": response.status_code,
        "added_count": len(blocks) if response.status_code == 200 else 0,
        "error": None if response.status_code == 200 else response.text
    }