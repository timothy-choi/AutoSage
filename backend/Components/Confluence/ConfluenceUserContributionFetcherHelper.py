import requests
from config import CONFLUENCE_API_BASE, CONFLUENCE_API_HEADERS

def fetch_user_pages(user_account_id: str, limit: int = 25) -> dict:
    url = (
        f"{CONFLUENCE_API_BASE}/search"
        f"?cql=creator={user_account_id}+order+by+lastmodified"
        f"&limit={limit}"
    )
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    return response.json().get("results", [])

def fetch_user_updates(user_account_id: str, limit: int = 25) -> dict:
    url = (
        f"{CONFLUENCE_API_BASE}/audit"
        f"?searchString={user_account_id}&limit={limit}"
    )
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    return response.json().get("results", [])

def fetch_user_comments(user_account_id: str, limit: int = 25) -> dict:
    url = (
        f"{CONFLUENCE_API_BASE}/search"
        f"?cql=type=comment+and+creator={user_account_id}+order+by+lastmodified"
        f"&limit={limit}"
    )
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    return response.json().get("results", [])

def get_user_contributions(user_account_id: str, limit: int = 25) -> dict:
    try:
        pages = fetch_user_pages(user_account_id, limit)
        comments = fetch_user_comments(user_account_id, limit)
        updates = fetch_user_updates(user_account_id, limit)

        return {
            "success": True,
            "contributions": {
                "pages_created": pages,
                "comments_posted": comments,
                "activities_logged": updates,
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}