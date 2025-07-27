import requests
from config import CONFLUENCE_API_BASE, CONFLUENCE_AUTH_HEADERS

def get_page_children(page_id: str) -> list:
    url = f"{CONFLUENCE_API_BASE}/content/{page_id}/child/page?limit=100"
    response = requests.get(url, headers=CONFLUENCE_AUTH_HEADERS)

    if response.status_code != 200:
        return []

    children_data = response.json().get("results", [])
    children = []

    for child in children_data:
        child_node = {
            "id": child["id"],
            "title": child["title"],
            "children": get_page_children(child["id"])
        }
        children.append(child_node)

    return children

def export_content_tree(space_key: str = None, root_page_id: str = None) -> dict:
    if root_page_id:
        root_url = f"{CONFLUENCE_API_BASE}/content/{root_page_id}"
    elif space_key:
        root_url = f"{CONFLUENCE_API_BASE}/space/{space_key}?expand=homepage"
    else:
        return {"success": False, "message": "Either 'space_key' or 'root_page_id' is required."}

    root_response = requests.get(root_url, headers=CONFLUENCE_AUTH_HEADERS)

    if root_response.status_code != 200:
        return {"success": False, "message": "Failed to retrieve root content.", "details": root_response.text}

    if root_page_id:
        root_data = root_response.json()
    else:
        root_data = root_response.json()["homepage"]

    tree = {
        "id": root_data["id"],
        "title": root_data["title"],
        "children": get_page_children(root_data["id"])
    }

    return {"success": True, "tree": tree}