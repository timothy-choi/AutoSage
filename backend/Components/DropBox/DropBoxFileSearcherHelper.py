import requests

DROPBOX_SEARCH_URL = "https://api.dropboxapi.com/2/files/search_v2"

def search_files_in_dropbox(
    access_token: str,
    query: str,
    path: str = "",
    max_results: int = 10,
    file_extensions: list[str] = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    options = {
        "path": path,
        "max_results": max_results,
        "filename_only": False
    }

    if file_extensions:
        options["file_extensions"] = file_extensions

    payload = {
        "query": query,
        "options": options
    }

    response = requests.post(DROPBOX_SEARCH_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Dropbox search failed: {response.text}")

    matches = response.json().get("matches", [])
    return {
        "query": query,
        "results": [
            {
                "name": match["metadata"]["metadata"]["name"],
                "path_display": match["metadata"]["metadata"]["path_display"],
                "id": match["metadata"]["metadata"]["id"]
            }
            for match in matches
        ]
    }