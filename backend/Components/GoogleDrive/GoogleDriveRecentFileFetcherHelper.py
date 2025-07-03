import requests

DRIVE_API_URL = "https://www.googleapis.com/drive/v3/files"

def fetch_recent_files(
    access_token: str,
    max_results: int = 10,
    sort_by: str = "modifiedTime"
) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "q": "trashed = false",
        "fields": (
            "files(id, name, mimeType, size, webViewLink, "
            "createdTime, modifiedTime, owners(emailAddress,displayName))"
        ),
        "pageSize": max_results,
        "orderBy": f"{sort_by} desc"
    }

    response = requests.get(DRIVE_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch recent files: {response.text}")

    return response.json().get("files", [])