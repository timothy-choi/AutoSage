import requests

CHANGES_URL = "https://www.googleapis.com/drive/v3/changes"
ABOUT_URL = "https://www.googleapis.com/drive/v3/about"

def get_start_page_token(access_token: str) -> str:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"fields": "startPageToken"}
    res = requests.get(ABOUT_URL, headers=headers, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed to get startPageToken: {res.text}")
    return res.json()["startPageToken"]

def fetch_drive_changes(
    access_token: str,
    start_page_token: str,
    max_results: int = 100
) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "pageToken": start_page_token,
        "pageSize": max_results,
        "fields": "changes(fileId,file(name,mimeType,trashed,modifiedTime,owners(emailAddress))),newStartPageToken"
    }

    res = requests.get(CHANGES_URL, headers=headers, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch changes: {res.text}")

    data = res.json()
    changes = data.get("changes", [])
    new_token = data.get("newStartPageToken", start_page_token)

    return {
        "status": "success",
        "startPageToken": start_page_token,
        "newStartPageToken": new_token,
        "changes": changes
    }