import requests

DROPBOX_CREATE_FOLDER_URL = "https://api.dropboxapi.com/2/files/create_folder_v2"

def create_dropbox_folder(
    access_token: str,
    folder_path: str,
    autorename: bool = False
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": folder_path,
        "autorename": autorename
    }

    response = requests.post(DROPBOX_CREATE_FOLDER_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to create folder: {response.text}")

    data = response.json()
    metadata = data.get("metadata", {})
    return {
        "status": "created",
        "name": metadata.get("name"),
        "path_display": metadata.get("path_display"),
        "id": metadata.get("id")
    }