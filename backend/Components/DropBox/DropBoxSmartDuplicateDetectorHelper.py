import requests
from typing import List, Dict

DROPBOX_LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"

def list_files_recursive(access_token: str, path: str = "") -> List[dict]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    files = []
    has_more = True
    payload = {
        "path": path,
        "recursive": True,
        "include_deleted": False
    }

    while has_more:
        response = requests.post(DROPBOX_LIST_FOLDER_URL, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to list folder: {response.text}")

        result = response.json()
        entries = result.get("entries", [])
        files.extend([f for f in entries if f[".tag"] == "file"])

        has_more = result.get("has_more", False)
        if has_more:
            payload = {
                "cursor": result["cursor"]
            }
            DROPBOX_CONTINUE_URL = "https://api.dropboxapi.com/2/files/list_folder/continue"
            response = requests.post(DROPBOX_CONTINUE_URL, headers=headers, json=payload)
            result = response.json()
            entries = result.get("entries", [])
            files.extend([f for f in entries if f[".tag"] == "file"])
            has_more = result.get("has_more", False)

    return files

def find_duplicate_files(files: List[dict], match_on: str = "content_hash") -> List[List[dict]]:
    """
    match_on: "name" or "content_hash"
    """
    from collections import defaultdict

    buckets: Dict[str, List[dict]] = defaultdict(list)

    for f in files:
        key = f["name"] if match_on == "name" else f.get("content_hash")
        if key:
            buckets[key].append(f)

    duplicates = [group for group in buckets.values() if len(group) > 1]
    return duplicates

def smart_detect_dropbox_duplicates(access_token: str, folder_path: str = "", match_on: str = "content_hash") -> dict:
    files = list_files_recursive(access_token, folder_path)
    duplicates = find_duplicate_files(files, match_on=match_on)

    formatted = []
    for group in duplicates:
        formatted.append([{
            "name": f["name"],
            "path": f["path_display"],
            "size": f["size"],
            "content_hash": f.get("content_hash")
        } for f in group])

    return {
        "match_on": match_on,
        "duplicate_groups": formatted,
        "total_duplicates": sum(len(g) for g in formatted)
    }