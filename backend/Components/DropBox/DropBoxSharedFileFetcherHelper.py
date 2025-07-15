import requests
from typing import List, Optional

DROPBOX_LIST_SHARED_LINKS_URL = "https://api.dropboxapi.com/2/sharing/list_shared_links"

def fetch_dropbox_shared_files(
    access_token: str,
    path: Optional[str] = None,
    direct_only: bool = False
) -> List[dict]:
    """
    Fetch a list of shared Dropbox files and folders.

    Args:
        access_token: Dropbox OAuth access token
        path: Optional filter by file/folder path
        direct_only: Whether to include only directly shared links (not inherited)

    Returns:
        A list of shared files/folders with metadata
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "direct_only": direct_only
    }

    if path:
        payload["path"] = path

    res = requests.post(DROPBOX_LIST_SHARED_LINKS_URL, headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Dropbox API error: {res.text}")

    data = res.json()
    links = data.get("links", [])

    shared_files = []
    for link in links:
        shared_files.append({
            "name": link.get("name"),
            "url": link.get("url"),
            "path": link.get("path_lower"),
            "visibility": link.get("link_permissions", {}).get("visibility", {}).get(".tag"),
            "type": link.get(".tag")
        })

    return shared_files