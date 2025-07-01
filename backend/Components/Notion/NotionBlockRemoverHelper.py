import requests

NOTION_BLOCKS_API = "https://api.notion.com/v1/blocks"
NOTION_VERSION = "2022-06-28"

def delete_notion_block(notion_token: str, block_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "archived": True
    }

    response = requests.patch(
        f"{NOTION_BLOCKS_API}/{block_id}",
        headers=headers,
        json=payload
    )

    return {
        "status": response.status_code,
        "block_id": block_id,
        "archived": response.status_code == 200,
        "error": None if response.status_code == 200 else response.text
    }