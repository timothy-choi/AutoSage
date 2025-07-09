import requests
from datetime import datetime, timedelta
from typing import List

DROPBOX_DELETE_URL = "https://api.dropboxapi.com/2/files/delete_v2"
DROPBOX_METADATA_URL = "https://api.dropboxapi.com/2/files/get_metadata"
DROPBOX_MOVE_URL = "https://api.dropboxapi.com/2/files/move_v2"


def delete_file_from_dropbox(access_token: str, path: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {"path": path}
    response = requests.post(DROPBOX_DELETE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Dropbox deletion failed: {response.text}")

    metadata = response.json().get("metadata", {})
    return {
        "status": "deleted",
        "name": metadata.get("name"),
        "path_display": metadata.get("path_display"),
        "id": metadata.get("id")
    }


def delete_multiple_files_from_dropbox(access_token: str, paths: List[str]) -> List[dict]:
    results = []
    for path in paths:
        try:
            result = delete_file_from_dropbox(access_token, path)
            results.append({"path": path, "status": "deleted", "id": result["id"]})
        except Exception as e:
            results.append({"path": path, "status": "error", "error": str(e)})
    return results


def delete_if_older_than(access_token: str, path: str, min_age_days: int) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(DROPBOX_METADATA_URL, headers=headers, json={"path": path})
    if response.status_code != 200:
        raise Exception(f"Metadata fetch failed: {response.text}")

    metadata = response.json()
    server_modified = metadata.get("server_modified")
    if not server_modified:
        raise Exception("Modified time unavailable.")

    modified_time = datetime.fromisoformat(server_modified.replace("Z", "+00:00"))
    if datetime.utcnow() - modified_time >= timedelta(days=min_age_days):
        return delete_file_from_dropbox(access_token, path)
    else:
        return {"status": "skipped", "reason": f"Not older than {min_age_days} days"}


def soft_delete_file(access_token: str, path: str, trash_folder: str = "/Trash") -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    filename = path.split("/")[-1]
    new_path = f"{trash_folder}/{filename}"

    payload = {"from_path": path, "to_path": new_path, "autorename": True}
    response = requests.post(DROPBOX_MOVE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Soft delete failed: {response.text}")

    metadata = response.json().get("metadata", {})
    return {
        "status": "moved_to_trash",
        "from": path,
        "to": metadata.get("path_display", new_path),
        "id": metadata.get("id")
    }


def should_ai_delete(name: str, size_bytes: int = 0) -> bool:
    keywords = ["temp", "backup", "old", "copy"]
    return size_bytes > 10_000_000 or any(k in name.lower() for k in keywords)