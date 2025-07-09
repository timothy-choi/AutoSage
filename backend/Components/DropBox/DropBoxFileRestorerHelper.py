import requests

DROPBOX_RESTORE_URL = "https://api.dropboxapi.com/2/files/restore"
DROPBOX_LIST_REVISIONS_URL = "https://api.dropboxapi.com/2/files/list_revisions"

def restore_file_to_revision(access_token: str, path: str, rev: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": path,
        "rev": rev
    }

    response = requests.post(DROPBOX_RESTORE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Restore failed: {response.text}")

    metadata = response.json()
    return {
        "status": "restored",
        "path": metadata.get("path_display"),
        "rev": metadata.get("rev"),
        "size": metadata.get("size")
    }

def list_file_revisions(access_token: str, path: str, limit: int = 10) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": path,
        "limit": limit
    }

    response = requests.post(DROPBOX_LIST_REVISIONS_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"List revisions failed: {response.text}")

    data = response.json()
    revisions = data.get("entries", [])
    return {
        "path": path,
        "revisions": [
            {
                "rev": r.get("rev"),
                "client_modified": r.get("client_modified"),
                "server_modified": r.get("server_modified"),
                "size": r.get("size")
            } for r in revisions
        ]
    }