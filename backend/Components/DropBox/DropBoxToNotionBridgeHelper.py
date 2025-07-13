import requests
from datetime import datetime
from typing import List, Optional

DROPBOX_LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def fetch_dropbox_files(access_token: str, folder_path: str = "", limit: Optional[int] = 50) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "path": folder_path,
        "recursive": False,
        "include_deleted": False,
        "limit": limit
    }
    res = requests.post(DROPBOX_LIST_FOLDER_URL, headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Dropbox API error: {res.text}")
    entries = res.json().get("entries", [])
    return [e for e in entries if e[".tag"] == "file"]

def create_notion_page(notion_token: str, database_id: str, file_info: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    properties = {
        "Name": {
            "title": [{"text": {"content": file_info["name"]}}]
        },
        "Path": {
            "rich_text": [{"text": {"content": file_info["path_display"]}}]
        },
        "Size (bytes)": {
            "number": file_info["size"]
        },
        "Upload Date": {
            "date": {"start": file_info["client_modified"]}
        }
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    res = requests.post(NOTION_API_URL, headers=headers, json=data)
    if res.status_code not in (200, 201):
        raise Exception(f"Notion API error: {res.text}")
    return res.json()

def bridge_dropbox_to_notion(
    dropbox_token: str,
    notion_token: str,
    notion_database_id: str,
    folder_path: str = "",
    max_files: int = 20
) -> dict:
    files = fetch_dropbox_files(dropbox_token, folder_path, max_files)
    created_pages = []
    for f in files:
        page = create_notion_page(notion_token, notion_database_id, f)
        created_pages.append({
            "file_name": f["name"],
            "notion_page_id": page.get("id")
        })
    return {
        "files_processed": len(files),
        "notion_pages_created": len(created_pages),
        "details": created_pages
    }