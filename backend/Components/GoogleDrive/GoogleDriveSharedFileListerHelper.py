import requests
import csv
from io import StringIO

DRIVE_API_URL = "https://www.googleapis.com/drive/v3/files"

def list_shared_with_me_files(
    access_token: str,
    max_results: int = 20
) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "q": "sharedWithMe and trashed = false",
        "fields": "files(id, name, mimeType, size, owners(emailAddress,displayName), webViewLink)",
        "pageSize": max_results
    }

    response = requests.get(DRIVE_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list shared files: {response.text}")

    return response.json().get("files", [])

def list_files_shared_by_me(
    access_token: str,
    max_results: int = 20
) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "q": "trashed = false",
        "fields": "files(id,name,mimeType,size,owners,emailAddress,permissions,webViewLink)",
        "pageSize": max_results
    }

    response = requests.get(DRIVE_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list files: {response.text}")

    all_files = response.json().get("files", [])
    shared_by_me = []

    for file in all_files:
        owners = [o["emailAddress"] for o in file.get("owners", [])]
        permissions = file.get("permissions", [])
        for perm in permissions:
            if perm.get("type") in ["anyone", "user", "group"] and perm.get("emailAddress") not in owners:
                shared_by_me.append(file)
                break

    return shared_by_me

def sort_files(files, sort_by="name", order="asc"):
    reverse = order == "desc"
    return sorted(files, key=lambda f: f.get(sort_by, ""), reverse=reverse)

def files_to_csv(files):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Type", "Size", "Owner", "Link"])
    for f in files:
        writer.writerow([
            f.get("id"),
            f.get("name"),
            f.get("mimeType"),
            f.get("size"),
            ",".join([o["emailAddress"] for o in f.get("owners", [])]),
            f.get("webViewLink")
        ])
    return output.getvalue()