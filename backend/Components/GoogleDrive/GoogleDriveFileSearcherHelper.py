import requests
from typing import List, Optional

GOOGLE_DRIVE_SEARCH_URL = "https://www.googleapis.com/drive/v3/files"

def search_drive_files(
    access_token: str,
    name_query: Optional[str] = None,
    mime_type: Optional[str] = None,
    custom_q: Optional[str] = None,
    max_results: int = 10
) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    query_parts = []

    if custom_q:
        query_parts.append(custom_q)
    else:
        if name_query:
            query_parts.append(f"name contains '{name_query}'")
        if mime_type:
            query_parts.append(f"mimeType = '{mime_type}'")
        query_parts.append("trashed = false")

    query = " and ".join(query_parts)

    params = {
        "q": query,
        "pageSize": max_results,
        "fields": "files(id, name, mimeType, modifiedTime, size, webViewLink)"
    }

    response = requests.get(GOOGLE_DRIVE_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Drive search failed: {response.text}")

    return response.json().get("files", [])