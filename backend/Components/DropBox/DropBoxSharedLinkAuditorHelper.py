import requests
from typing import Optional

DROPBOX_LIST_SHARED_LINKS_URL = "https://api.dropboxapi.com/2/sharing/list_shared_links"

def audit_dropbox_shared_links(access_token: str, path: Optional[str] = None) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": path,
        "direct_only": False
    } if path else {}

    response = requests.post(DROPBOX_LIST_SHARED_LINKS_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to list shared links: {response.text}")

    links = response.json().get("links", [])

    audited_links = []
    for link in links:
        metadata = link.get("link_permissions", {})
        visibility = metadata.get("requested_visibility", {}).get(".tag")
        audience = metadata.get("audience", {}).get(".tag")
        access_level = metadata.get("access", {}).get(".tag")

        audited_links.append({
            "name": link.get("name"),
            "path": link.get("path_lower"),
            "url": link.get("url"),
            "visibility": visibility,
            "audience": audience,
            "access": access_level,
            "expires": link.get("expires")
        })

    return {
        "total_links": len(audited_links),
        "shared_links": audited_links
    }