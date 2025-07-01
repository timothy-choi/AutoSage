import requests

NOTION_BLOCKS_API = "https://api.notion.com/v1/blocks"
NOTION_VERSION = "2022-06-28"

def edit_notion_block(notion_token: str, block_id: str, block_type: str, new_text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        block_type: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": new_text
                    }
                }
            ]
        }
    }

    response = requests.patch(
        f"{NOTION_BLOCKS_API}/{block_id}",
        headers=headers,
        json=payload
    )

    return {
        "status": response.status_code,
        "block_id": block_id,
        "updated_text": new_text if response.status_code == 200 else None,
        "error": None if response.status_code == 200 else response.text
    }