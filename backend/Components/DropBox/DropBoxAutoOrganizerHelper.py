import requests
import os
from datetime import datetime

LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"
MOVE_URL = "https://api.dropboxapi.com/2/files/move_v2"

def list_files_in_folder(access_token: str, folder_path: str = "") -> list:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "path": folder_path,
        "recursive": False,
        "include_media_info": False,
        "include_deleted": False
    }

    response = requests.post(LIST_FOLDER_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to list folder: {response.text}")

    return response.json().get("entries", [])


def determine_target_path(file_name: str, client_modified: str, base_folder: str = "") -> str:
    ext = os.path.splitext(file_name)[1].lower()
    date = datetime.fromisoformat(client_modified.rstrip("Z"))

    if ext in [".pdf", ".docx", ".txt"]:
        folder = "Documents"
    elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
        folder = "Images"
    elif ext in [".mp4", ".mov"]:
        folder = "Videos"
    elif "invoice" in file_name.lower():
        folder = "Finance"
    else:
        folder = "Other"

    date_folder = date.strftime("%Y/%B")
    return f"{base_folder}/{folder}/{date_folder}/{file_name}"


def move_file(access_token: str, from_path: str, to_path: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "from_path": from_path,
        "to_path": to_path,
        "allow_ownership_transfer": False,
        "autorename": True
    }

    response = requests.post(MOVE_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Move failed: {response.text}")

    return {
        "from": from_path,
        "to": to_path,
        "status": "moved"
    }


def auto_organize_dropbox_files(access_token: str, folder_path: str = "") -> dict:
    files = list_files_in_folder(access_token, folder_path)
    moved = []

    for entry in files:
        if entry[".tag"] != "file":
            continue

        from_path = entry["path_lower"]
        file_name = entry["name"]
        modified = entry["client_modified"]

        to_path = determine_target_path(file_name, modified, base_folder=folder_path)
        result = move_file(access_token, from_path, to_path)
        moved.append(result)

    return {
        "folder": folder_path or "/",
        "files_moved": len(moved),
        "details": moved
    }