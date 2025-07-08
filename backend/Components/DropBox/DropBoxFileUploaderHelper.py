import os
import requests

DROPBOX_UPLOAD_URL = "https://content.dropboxapi.com/2/files/upload"

def upload_file_to_dropbox(
    access_token: str,
    local_file_path: str,
    dropbox_dest_path: str,
    mode: str = "add" 
) -> dict:
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"File not found: {local_file_path}")

    with open(local_file_path, "rb") as f:
        file_content = f.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": str({
            "path": dropbox_dest_path,
            "mode": mode,
            "autorename": True,
            "mute": False,
            "strict_conflict": False
        }).replace("'", '"'),
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(DROPBOX_UPLOAD_URL, headers=headers, data=file_content)

    if response.status_code != 200:
        raise Exception(f"Dropbox upload failed: {response.text}")

    return response.json()