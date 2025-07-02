import requests

DRIVE_API_URL = "https://www.googleapis.com/drive/v3/files/{}"

def move_file_to_folder(access_token: str, file_id: str, target_folder_id: str) -> dict:
    metadata_url = DRIVE_API_URL.format(file_id)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    metadata_response = requests.get(metadata_url, headers=headers, params={"fields": "parents"})
    if metadata_response.status_code != 200:
        raise Exception(f"Failed to fetch file metadata: {metadata_response.text}")

    current_parents = ",".join(metadata_response.json().get("parents", []))

    update_params = {
        "addParents": target_folder_id,
        "removeParents": current_parents,
        "fields": "id, parents"
    }

    update_response = requests.patch(metadata_url, headers=headers, params=update_params)
    if update_response.status_code != 200:
        raise Exception(f"Failed to move file: {update_response.text}")

    return {
        "status": "success",
        "file_id": file_id,
        "new_parents": update_response.json().get("parents", [])
    }