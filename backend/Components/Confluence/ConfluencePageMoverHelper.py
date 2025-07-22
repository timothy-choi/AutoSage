import requests

def move_confluence_page(base_url, username, api_token, page_id, new_parent_id):
    get_url = f"{base_url}/rest/api/content/{page_id}?expand=version"
    auth = (username, api_token)
    headers = {
        "Content-Type": "application/json"
    }

    get_resp = requests.get(get_url, auth=auth, headers=headers)
    get_resp.raise_for_status()
    page_data = get_resp.json()
    version = page_data["version"]["number"]
    title = page_data["title"]

    update_url = f"{base_url}/rest/api/content/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {
            "number": version + 1
        },
        "ancestors": [{"id": new_parent_id}]
    }

    update_resp = requests.put(update_url, auth=auth, headers=headers, json=payload)
    update_resp.raise_for_status()
    return update_resp.json()