import requests
from typing import List, Optional

LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"
CONTINUE_URL = "https://api.dropboxapi.com/2/files/list_folder/continue"

def fetch_new_uploads(access_token: str, cursor: Optional[str] = None, folder_path: str = "") -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    if cursor:
        payload = { "cursor": cursor }
        url = CONTINUE_URL
    else:
        payload = {
            "path": folder_path,
            "recursive": True,
            "include_media_info": False,
            "include_deleted": False
        }
        url = LIST_FOLDER_URL

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Dropbox API error: {response.text}")

    result = response.json()
    new_files = [entry for entry in result.get("entries", []) if entry[".tag"] == "file"]

    return {
        "new_files": new_files,
        "new_cursor": result.get("cursor"),
        "has_more": result.get("has_more", False)
    }

def send_console_notification(files: List[dict]):
    for f in files:
        print(f"[DROPBOX] 📥 New file uploaded: {f['name']} at {f['path_display']} (size: {f['size']} bytes)")

def notify_new_uploads(access_token: str, cursor: Optional[str] = None, folder_path: str = "") -> dict:
    result = fetch_new_uploads(access_token, cursor, folder_path)
    new_files = result["new_files"]

    if new_files:
        send_console_notification(new_files)

    return {
        "new_uploads_detected": len(new_files),
        "new_cursor": result["new_cursor"],
        "files": [
            {
                "name": f["name"],
                "path": f["path_display"],
                "size": f["size"],
                "client_modified": f["client_modified"]
            } for f in new_files
        ]
    }