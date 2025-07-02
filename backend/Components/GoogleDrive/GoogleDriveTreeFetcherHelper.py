import requests

GOOGLE_DRIVE_SEARCH_URL = "https://www.googleapis.com/drive/v3/files"

def fetch_folder_tree(access_token: str, folder_id: str, recursive: bool = True) -> dict:
    def fetch_children(parent_id):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "q": f"'{parent_id}' in parents and trashed = false",
            "fields": "files(id, name, mimeType)",
            "pageSize": 1000
        }

        response = requests.get(GOOGLE_DRIVE_SEARCH_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch children: {response.text}")

        items = response.json().get("files", [])

        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder" and recursive:
                item["children"] = fetch_children(item["id"])

        return items

    tree = {
        "id": folder_id,
        "name": "root",
        "mimeType": "application/vnd.google-apps.folder",
        "children": fetch_children(folder_id)
    }
    return tree