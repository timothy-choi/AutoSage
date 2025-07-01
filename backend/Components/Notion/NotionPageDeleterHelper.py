import requests

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def delete_notion_page(notion_token: str, page_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "archived": True
    }

    response = requests.patch(f"{NOTION_API_URL}/{page_id}", headers=headers, json=payload)

    return {
        "status": response.status_code,
        "archived": response.status_code == 200,
        "error": None if response.status_code == 200 else response.text
    }