import requests
from typing import Dict, Any, List

def fetch_confluence_page(base_url: str, username: str, api_token: str, page_id: str) -> Dict[str, Any]:
    url = f"{base_url}/rest/api/content/{page_id}"
    response = requests.get(url, auth=(username, api_token))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch page {page_id}: {response.text}")

def fetch_confluence_pages_by_space(base_url: str, username: str, api_token: str, space_key: str, limit: int = 25) -> List[Dict[str, Any]]:
    url = f"{base_url}/rest/api/content"
    params = {
        "spaceKey": space_key,
        "limit": limit,
        "expand": "body.storage,version"
    }
    response = requests.get(url, auth=(username, api_token), params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception(f"Failed to fetch pages from space {space_key}: {response.text}")