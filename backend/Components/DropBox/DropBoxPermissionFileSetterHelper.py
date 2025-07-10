import requests
from typing import Optional

DROPBOX_MODIFY_LINK_URL = "https://api.dropboxapi.com/2/sharing/modify_shared_link_settings"
DROPBOX_LIST_SHARED_LINKS_URL = "https://api.dropboxapi.com/2/sharing/list_shared_links"

def get_shared_link_url(access_token: str, path: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(DROPBOX_LIST_SHARED_LINKS_URL, headers=headers, json={"path": path})

    if response.status_code != 200:
        raise Exception(f"Failed to fetch shared links: {response.text}")

    links = response.json().get("links", [])
    if not links:
        raise Exception(f"No shared link found for: {path}")

    return links[0]["url"]


def set_dropbox_file_permissions(
    access_token: str,
    path: str,
    requested_visibility: str = "public",  # "public", "team_only", "password"
    allow_download: bool = True,
    password: Optional[str] = None,
    expires: Optional[str] = None           # ISO8601
) -> dict:
    shared_link_url = get_shared_link_url(access_token, path)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    settings = {
        "requested_visibility": requested_visibility,
        "access": "viewer" if allow_download else "viewer_no_download"
    }

    if password:
        settings["link_password"] = password

    if expires:
        settings["expires"] = expires

    payload = {
        "url": shared_link_url,
        "settings": settings
    }

    response = requests.post(DROPBOX_MODIFY_LINK_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Permission update failed: {response.text}")

    return {
        "status": "updated",
        "path": path,
        "shared_link_url": shared_link_url,
        "visibility": requested_visibility,
        "expires": expires
    }