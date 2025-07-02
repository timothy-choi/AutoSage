import requests

GOOGLE_DRIVE_CREATE_URL = "https://www.googleapis.com/drive/v3/files"

def create_drive_folder(access_token: str, folder_name: str, parent_folder_id: str = None) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }

    if parent_folder_id:
        metadata["parents"] = [parent_folder_id]

    response = requests.post(GOOGLE_DRIVE_CREATE_URL, headers=headers, json=metadata)

    if response.status_code not in (200, 201):
        raise Exception(f"Folder creation failed: {response.text}")

    return {
        "status": "success",
        "folder_id": response.json().get("id"),
        "folder_name": response.json().get("name")
    }