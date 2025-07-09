import requests
from typing import Optional

DROPBOX_CREATE_LINK_URL = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"

def generate_dropbox_shared_link(
    access_token: str,
    path: str,
    visibility: Optional[str] = "public",        
    allow_download: Optional[bool] = True,
    password: Optional[str] = None,
    expires: Optional[str] = None               
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    settings = {
        "requested_visibility": visibility,
        "audience": "public",
        "access": "viewer" if allow_download else "viewer_no_download"
    }

    if password:
        settings["link_password"] = password

    if expires:
        settings["expires"] = expires

    payload = {
        "path": path,
        "settings": settings
    }

    response = requests.post(DROPBOX_CREATE_LINK_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to create shared link: {response.text}")

    data = response.json()
    return {
        "url": data.get("url"),
        "id": data.get("id"),
        "visibility": data.get("link_permissions", {}).get("requested_visibility", {}).get(".tag"),
        "expires": data.get("expires")
    }