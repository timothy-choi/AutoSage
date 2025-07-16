import requests
from typing import Optional
from datetime import datetime

DROPBOX_QUOTA_URL = "https://api.dropboxapi.com/2/users/get_space_usage"
DROPBOX_LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"
DROPBOX_CONTINUE_URL = "https://api.dropboxapi.com/2/files/list_folder/continue"

def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def get_quota(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(DROPBOX_QUOTA_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Quota fetch error: {response.text}")
    data = response.json()
    used = data["used"]
    allocated = data["allocation"]["allocated"]
    return used, allocated

def list_all_files(access_token: str, path: str = "") -> list:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "path": path,
        "recursive": True,
        "include_media_info": False,
        "include_deleted": False
    }
    res = requests.post(DROPBOX_LIST_FOLDER_URL, headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Folder listing failed: {res.text}")
    data = res.json()
    entries = data.get("entries", [])
    cursor = data.get("cursor")

    while data.get("has_more"):
        res = requests.post(DROPBOX_CONTINUE_URL, headers=headers, json={"cursor": cursor})
        if res.status_code != 200:
            break
        data = res.json()
        entries.extend(data.get("entries", []))
        cursor = data.get("cursor")
    
    return [f for f in entries if f[".tag"] == "file"]

def summarize_usage(files: list) -> dict:
    summary = {}
    total_size = 0
    for f in files:
        ext = f["name"].split(".")[-1].lower() if "." in f["name"] else "no_extension"
        summary[ext] = summary.get(ext, 0) + f["size"]
        total_size += f["size"]
    return {
        "total_file_count": len(files),
        "total_size_bytes": total_size,
        "size_by_type": summary
    }

def generate_usage_report(access_token: str, human_readable: bool = False) -> dict:
    used, allocated = get_quota(access_token)
    files = list_all_files(access_token)
    summary = summarize_usage(files)

    if human_readable:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_quota": format_bytes(allocated),
            "used_storage": format_bytes(used),
            "usage_percent": f"{used / allocated * 100:.2f}%",
            "total_file_count": summary["total_file_count"],
            "total_file_size": format_bytes(summary["total_size_bytes"]),
            "size_by_type": {
                k: format_bytes(v) for k, v in summary["size_by_type"].items()
            }
        }
    else:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_quota_bytes": allocated,
            "used_storage_bytes": used,
            "usage_percent": used / allocated * 100,
            "total_file_count": summary["total_file_count"],
            "total_file_size_bytes": summary["total_size_bytes"],
            "size_by_type_bytes": summary["size_by_type"]
        }