import requests

DRIVE_API_URL = "https://www.googleapis.com/drive/v3/files/{file_id}"
PERMISSIONS_API_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/permissions"

def generate_shared_link(access_token: str, file_id: str, role: str = "reader") -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    permission_payload = {
        "type": "anyone",
        "role": role
    }

    perm_res = requests.post(
        PERMISSIONS_API_URL.format(file_id=file_id),
        headers=headers,
        json=permission_payload
    )

    if perm_res.status_code not in (200, 201):
        raise Exception(f"Permission failed: {perm_res.text}")

    metadata_res = requests.get(
        DRIVE_API_URL.format(file_id=file_id),
        headers=headers,
        params={"fields": "id, name, webViewLink"}
    )

    if metadata_res.status_code != 200:
        raise Exception(f"Failed to fetch metadata: {metadata_res.text}")

    data = metadata_res.json()
    return {
        "status": "success",
        "file_id": data["id"],
        "file_name": data["name"],
        "webViewLink": data.get("webViewLink")
    }