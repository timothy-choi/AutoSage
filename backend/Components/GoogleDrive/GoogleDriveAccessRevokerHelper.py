import requests

PERMISSIONS_LIST_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/permissions"
PERMISSIONS_DELETE_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/permissions/{permission_id}"

def list_drive_permissions(access_token: str, file_id: str) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(PERMISSIONS_LIST_URL.format(file_id=file_id), headers=headers, params={
        "fields": "permissions(id, type, role, emailAddress)"
    })
    if response.status_code != 200:
        raise Exception(f"Failed to list permissions: {response.text}")
    return response.json().get("permissions", [])

def revoke_drive_permission(access_token: str, file_id: str, permission_id: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(PERMISSIONS_DELETE_URL.format(file_id=file_id, permission_id=permission_id), headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to revoke permission: {response.text}")
    return {
        "status": "success",
        "file_id": file_id,
        "revoked_permission_id": permission_id
    }