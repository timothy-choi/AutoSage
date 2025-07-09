import requests

DROPBOX_MOVE_URL = "https://api.dropboxapi.com/2/files/move_v2"

def move_file_in_dropbox(
    access_token: str,
    from_path: str,
    to_path: str,
    autorename: bool = False
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "from_path": from_path,
        "to_path": to_path,
        "autorename": autorename
    }

    response = requests.post(DROPBOX_MOVE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Dropbox move failed: {response.text}")

    metadata = response.json().get("metadata", {})
    return {
        "status": "moved",
        "from": from_path,
        "to": metadata.get("path_display", to_path),
        "id": metadata.get("id")
    }