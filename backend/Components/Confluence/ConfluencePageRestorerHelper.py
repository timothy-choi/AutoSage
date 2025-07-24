import requests

def restore_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str
) -> dict:
    url = f"{base_url}/rest/api/content/{page_id}"

    get_response = requests.get(url, auth=(username, api_token))
    if get_response.status_code != 200:
        raise Exception(f"Failed to retrieve trashed page {page_id}: {get_response.text}")
    
    page_data = get_response.json()

    version = page_data["version"]["number"] + 1

    payload = {
        "id": page_id,
        "type": page_data["type"],
        "title": page_data["title"],
        "space": {"key": page_data["space"]["key"]},
        "body": {
            "storage": {
                "value": page_data["body"]["storage"]["value"],
                "representation": "storage"
            }
        },
        "version": {
            "number": version,
            "message": "Restored from trash"
        },
        "status": "current"
    }

    headers = {
        "Content-Type": "application/json"
    }

    put_response = requests.put(url, json=payload, headers=headers, auth=(username, api_token))
    if put_response.status_code != 200:
        raise Exception(f"Failed to restore page {page_id}: {put_response.text}")
    
    return put_response.json()