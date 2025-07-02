import requests

GOOGLE_DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

def upload_file_to_drive(access_token: str, file_content: bytes, file_name: str, mime_type: str, parent_folder_id: str = None) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    metadata = {
        "name": file_name,
    }

    if parent_folder_id:
        metadata["parents"] = [parent_folder_id]

    multipart_data = {
        "metadata": (None, str(metadata).replace("'", '"'), "application/json"),
        "file": (file_name, file_content, mime_type)
    }

    response = requests.post(GOOGLE_DRIVE_UPLOAD_URL, headers=headers, files=multipart_data)

    if response.status_code not in (200, 201):
        raise Exception(f"File upload failed: {response.text}")

    return {
        "status": "success",
        "file_id": response.json().get("id"),
        "file_name": response.json().get("name"),
        "webViewLink": response.json().get("webViewLink", "https://drive.google.com/drive/u/0/my-drive")
    }