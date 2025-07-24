import requests
from typing import List

def add_labels_to_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    labels: List[str]
) -> dict:
    url = f"{base_url}/rest/api/content/{page_id}/label"
    auth = (username, api_token)
    headers = {"Content-Type": "application/json"}

    payload = [{"prefix": "global", "name": label} for label in labels]

    response = requests.post(url, auth=auth, headers=headers, json=payload)
    return {
        "status_code": response.status_code,
        "response": response.json() if response.content else {}
    }

def get_labels_of_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str
) -> dict:
    url = f"{base_url}/rest/api/content/{page_id}/label"
    auth = (username, api_token)

    response = requests.get(url, auth=auth)
    return {
        "status_code": response.status_code,
        "response": response.json() if response.content else {}
    }

def remove_label_from_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    label: str
) -> dict:
    url = f"{base_url}/rest/api/content/{page_id}/label/{label}"
    auth = (username, api_token)

    response = requests.delete(url, auth=auth)
    return {
        "status_code": response.status_code,
        "response": {"message": "Label removed" if response.status_code == 204 else response.text}
    }