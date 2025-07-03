import requests

DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
DRIVE_UPDATE_URL = "https://www.googleapis.com/drive/v3/files/{file_id}"

def list_files(access_token: str, max_results: int = 50):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": "trashed = false",
        "fields": "files(id, name, mimeType, size, parents)",
        "pageSize": max_results
    }
    r = requests.get(DRIVE_FILES_URL, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to list files: {r.text}")
    return r.json().get("files", [])

def create_folder(access_token: str, folder_name: str, parent_id=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        payload["parents"] = [parent_id]

    r = requests.post(DRIVE_FILES_URL, headers=headers, json=payload)
    if r.status_code not in (200, 201):
        raise Exception(f"Failed to create folder: {r.text}")
    return r.json()["id"]

def move_file(access_token: str, file_id: str, new_parent_id: str, old_parent_ids: list):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "addParents": new_parent_id,
        "removeParents": ",".join(old_parent_ids),
        "fields": "id, parents"
    }
    r = requests.patch(DRIVE_UPDATE_URL.format(file_id=file_id), headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to move file: {r.text}")
    return r.json()

def auto_organize_files(access_token: str, strategy: str = "type", max_results: int = 50) -> dict:
    files = list_files(access_token, max_results)
    created_folders = {}
    organized = []

    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            continue 

        if strategy == "type":
            key = file["mimeType"].split("/")[-1].capitalize()
        elif strategy == "size":
            size_mb = int(file.get("size", 0)) / (1024 * 1024)
            if size_mb > 100:
                key = "Large"
            elif size_mb > 10:
                key = "Medium"
            else:
                key = "Small"
        else:
            key = "Other"

        if key not in created_folders:
            folder_id = create_folder(access_token, key)
            created_folders[key] = folder_id
        else:
            folder_id = created_folders[key]

        move_file(access_token, file["id"], folder_id, file.get("parents", []))
        organized.append({"file": file["name"], "moved_to": key})

    return {
        "status": "success",
        "organized_files": organized,
        "created_folders": list(created_folders.keys())
    }