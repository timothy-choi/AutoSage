import requests

PERMISSION_URL = "https://www.googleapis.com/drive/v3/files/{}/permissions"

def set_drive_permission(
    access_token: str,
    file_id: str,
    role: str,
    permission_type: str,
    email_address: str = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    permission = {
        "type": permission_type,
        "role": role
    }

    if permission_type in ("user", "group"):
        if not email_address:
            raise Exception("Email address required for user or group permissions.")
        permission["emailAddress"] = email_address

    url = PERMISSION_URL.format(file_id)
    response = requests.post(url, headers=headers, json=permission)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to set permission: {response.status_code} - {response.text}")

    return {
        "status": "success",
        "file_id": file_id,
        "role": role,
        "type": permission_type,
        "granted_to": email_address if email_address else "anyone"
    }