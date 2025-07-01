import requests

NOTION_API_URL = "https://api.notion.com/v1/databases"
NOTION_VERSION = "2022-06-28"

def fetch_database_schema(notion_token: str, database_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer " + notion_token,
        "Notion-Version": NOTION_VERSION
    }

    response = requests.get(f"{NOTION_API_URL}/{database_id}", headers=headers)

    if response.status_code != 200:
        return {
            "status": response.status_code,
            "error": response.text,
            "properties": None
        }

    data = response.json()
    return {
        "status": 200,
        "database_id": database_id,
        "title": data.get("title", []),
        "properties": data.get("properties", {})
    }