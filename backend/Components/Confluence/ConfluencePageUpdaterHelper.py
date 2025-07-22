import requests

def update_confluence_page(base_url, username, api_token, page_id, new_title, new_content):
    get_url = f"{base_url}/rest/api/content/{page_id}?expand=version"
    auth = (username, api_token)
    headers = {
        "Content-Type": "application/json"
    }

    get_response = requests.get(get_url, auth=auth, headers=headers)
    get_response.raise_for_status()
    current_page = get_response.json()
    current_version = current_page["version"]["number"]

    update_url = f"{base_url}/rest/api/content/{page_id}"
    updated_data = {
        "id": page_id,
        "type": "page",
        "title": new_title,
        "version": {
            "number": current_version + 1
        },
        "body": {
            "storage": {
                "value": new_content,
                "representation": "storage"
            }
        }
    }

    update_response = requests.put(update_url, auth=auth, headers=headers, json=updated_data)
    update_response.raise_for_status()
    return update_response.json()