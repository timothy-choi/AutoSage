import requests
from collections import defaultdict

DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"

def list_files(access_token: str, max_results: int = 1000) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": "trashed = false",
        "fields": "files(id,name,mimeType,size,webViewLink)",
        "pageSize": max_results
    }

    response = requests.get(DRIVE_FILES_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch files: {response.text}")

    return response.json().get("files", [])

def find_duplicates(files: list, strategy: str = "name") -> dict:
    groups = defaultdict(list)

    for f in files:
        if strategy == "name":
            key = f.get("name", "").lower()
        elif strategy == "name+size":
            key = f"{f.get('name','').lower()}_{f.get('size','')}"
        elif strategy == "name+size+type":
            key = f"{f.get('name','').lower()}_{f.get('size','')}_{f.get('mimeType','')}"
        else:
            raise Exception(f"Unsupported strategy: {strategy}")

        groups[key].append(f)

    duplicates = {k: v for k, v in groups.items() if len(v) > 1}

    return {
        "status": "success",
        "strategy": strategy,
        "duplicate_groups": duplicates
    }

def find_drive_duplicates(
    access_token: str,
    strategy: str = "name",
    max_results: int = 1000
) -> dict:
    files = list_files(access_token, max_results)
    return find_duplicates(files, strategy)