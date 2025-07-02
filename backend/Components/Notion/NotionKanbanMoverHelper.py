import requests

NOTION_VERSION = "2022-06-28"
NOTION_PAGE_URL = "https://api.notion.com/v1/pages/{}"

def move_kanban_card(notion_token: str, page_id: str, new_status: str, status_property_name: str = "Status") -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    payload = {
        "properties": {
            status_property_name: {
                "select": {
                    "name": new_status
                }
            }
        }
    }

    response = requests.patch(NOTION_PAGE_URL.format(page_id), headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to move task in Kanban: {response.text}")

    return {
        "status": "success",
        "page_id": page_id,
        "new_status": new_status,
        "property": status_property_name
    }