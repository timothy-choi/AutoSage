import requests
from config import CONFLUENCE_API_BASE, CONFLUENCE_API_HEADERS, NOTION_API_BASE, NOTION_API_HEADERS

def fetch_confluence_page_content(page_id: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/content/{page_id}?expand=body.storage,title"
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    data = response.json()
    return {
        "title": data["title"],
        "body": data["body"]["storage"]["value"]
    }

def create_notion_page(notion_database_id: str, title: str, html_content: str) -> dict:
    notion_url = f"{NOTION_API_BASE}/pages"

    payload = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": title}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": html_content}}]
                }
            }
        ]
    }

    response = requests.post(notion_url, json=payload, headers=NOTION_API_HEADERS)
    if response.status_code != 200:
        return {"success": False, "error": response.text}
    return {"success": True, "data": response.json()}

def sync_confluence_to_notion(confluence_page_id: str, notion_database_id: str) -> dict:
    try:
        confluence_data = fetch_confluence_page_content(confluence_page_id)
        return create_notion_page(
            notion_database_id,
            confluence_data["title"],
            confluence_data["body"]
        )
    except Exception as e:
        return {"success": False, "error": str(e)}