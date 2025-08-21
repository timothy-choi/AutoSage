import requests

def create_notion_page(token: str, database_id: str, title: str, description: str = ""):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    { "text": { "content": title } }
                ]
            },
            "Description": {
                "rich_text": [
                    { "text": { "content": description } }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def extract_card_data(payload: dict):
    action = payload.get("action", {})
    type_ = action.get("type", "")
    if type_ != "createCard":
        return None

    data = action.get("data", {})
    card_name = data.get("card", {}).get("name", "")
    card_desc = data.get("card", {}).get("desc", "")
    return {
        "title": card_name,
        "description": card_desc
    }