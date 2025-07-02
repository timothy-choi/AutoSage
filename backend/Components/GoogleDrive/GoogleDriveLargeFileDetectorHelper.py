import requests

DRIVE_LIST_URL = "https://www.googleapis.com/drive/v3/files"

def detect_large_files(access_token: str, size_threshold_mb: int = 100, max_results: int = 20) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": "trashed = false and mimeType != 'application/vnd.google-apps.folder'",
        "fields": "files(id, name, size, mimeType, webViewLink)",
        "pageSize": 1000
    }

    response = requests.get(DRIVE_LIST_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list files: {response.text}")

    size_threshold_bytes = size_threshold_mb * 1024 * 1024
    files = response.json().get("files", [])

    large_files = [
        f for f in files
        if "size" in f and int(f["size"]) >= size_threshold_bytes
    ]

    sorted_files = sorted(large_files, key=lambda f: int(f["size"]), reverse=True)
    return sorted_files[:max_results]