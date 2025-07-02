import requests

GOOGLE_DRIVE_TRASH_URL = "https://www.googleapis.com/drive/v3/files/{}"

DRIVE_DELETE_URL = "https://www.googleapis.com/drive/v3/files/{}"

def delete_drive_file(access_token: str, file_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.delete(DRIVE_DELETE_URL.format(file_id), headers=headers)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"File {file_id} deleted successfully."
        }
    else:
        raise Exception(f"File deletion failed: {response.status_code} - {response.text}")

def trash_drive_file(access_token: str, file_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(
        GOOGLE_DRIVE_TRASH_URL.format(file_id),
        headers=headers,
        json={"trashed": True}
    )

    if response.status_code != 200:
        raise Exception(f"Failed to trash file: {response.text}")

    return {
        "status": "success",
        "message": f"File {file_id} moved to trash."
    }

def batch_delete_files(access_token: str, file_ids: list, permanent: bool = True) -> dict:
    results = []
    for fid in file_ids:
        try:
            if permanent:
                results.append(delete_drive_file(access_token, fid))
            else:
                results.append(trash_drive_file(access_token, fid))
        except Exception as e:
            results.append({"file_id": fid, "error": str(e)})
    return {"results": results}

def get_file_metadata(access_token: str, file_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"https://www.googleapis.com/drive/v3/files/{file_id}",
        headers=headers,
        params={"fields": "id,name,mimeType,modifiedTime,size"}
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch file metadata: {response.text}")
    return response.json()