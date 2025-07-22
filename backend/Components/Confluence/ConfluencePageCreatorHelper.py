import requests

def create_confluence_page(base_url, username, api_token, space_key, title, content, parent_id=None):
    url = f"{base_url}/rest/api/content"
    auth = (username, api_token)
    headers = {
        "Content-Type": "application/json"
    }

    page_data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if parent_id:
        page_data["ancestors"] = [{"id": str(parent_id)}]

    response = requests.post(url, auth=auth, headers=headers, json=page_data)
    response.raise_for_status()
    return response.json()