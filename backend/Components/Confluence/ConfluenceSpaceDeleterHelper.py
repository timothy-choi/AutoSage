import requests
from config import CONFLUENCE_API_BASE, CONFLUENCE_AUTH_HEADERS

def delete_confluence_space(space_key: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/space/{space_key}"
    response = requests.delete(url, headers=CONFLUENCE_AUTH_HEADERS)

    if response.status_code == 204:
        return {"success": True, "message": f"Space '{space_key}' successfully deleted."}
    elif response.status_code == 403:
        return {"success": False, "message": "Forbidden: You don't have permission to delete this space."}
    elif response.status_code == 404:
        return {"success": False, "message": f"Space '{space_key}' not found."}
    else:
        return {
            "success": False,
            "message": f"Failed to delete space '{space_key}'.",
            "status_code": response.status_code,
            "details": response.text
        }