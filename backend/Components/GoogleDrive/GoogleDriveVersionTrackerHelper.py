import requests

REVISIONS_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/revisions/{revision_id}"
LIST_REVISIONS_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/revisions"

def list_file_versions(access_token: str, file_id: str, max_results: int = 20) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "fields": "revisions(id, modifiedTime, keepForever, size, mimeType, originalFilename)",
        "pageSize": max_results
    }

    r = requests.get(LIST_REVISIONS_URL.format(file_id=file_id), headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch revisions: {r.text}")

    return {
        "status": "success",
        "file_id": file_id,
        "versions": r.json().get("revisions", [])
    }

def delete_revision(access_token: str, file_id: str, revision_id: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.delete(REVISIONS_URL.format(file_id=file_id, revision_id=revision_id), headers=headers)
    if r.status_code != 204:
        raise Exception(f"Failed to delete revision: {r.text}")
    return {
        "status": "success",
        "message": f"Revision {revision_id} deleted",
        "file_id": file_id
    }

def keep_forever_revision(access_token: str, file_id: str, revision_id: str, keep: bool = True) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {"keepForever": keep}
    r = requests.patch(REVISIONS_URL.format(file_id=file_id, revision_id=revision_id), headers=headers, json=body)
    if r.status_code != 200:
        raise Exception(f"Failed to update keepForever: {r.text}")
    return {
        "status": "success",
        "message": f"Revision {revision_id} keepForever set to {keep}",
        "file_id": file_id
    }