import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from typing import List, Optional

DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"

def download_dropbox_file(access_token: str, path: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": f'{{"path": "{path}"}}'
    }
    res = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Dropbox download error: {res.text}")
    return res.content

def upload_to_gdrive(
    creds: Credentials,
    file_name: str,
    file_bytes: bytes,
    mime_type: str = "application/octet-stream",
    parent_folder_id: Optional[str] = None
) -> dict:
    drive_service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": file_name}
    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    media = MediaInMemoryUpload(file_bytes, mimetype=mime_type)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, mimeType, parents"
    ).execute()
    return uploaded_file

def migrate_dropbox_files_to_gdrive(
    dropbox_token: str,
    gdrive_creds: Credentials,
    dropbox_paths: List[str],
    gdrive_folder_id: Optional[str] = None
) -> dict:
    migrated = []
    for path in dropbox_paths:
        file_bytes = download_dropbox_file(dropbox_token, path)
        file_name = path.split("/")[-1]

        ext = file_name.lower().split(".")[-1]
        mime_type = {
            "pdf": "application/pdf",
            "txt": "text/plain",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xls": "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }.get(ext, "application/octet-stream")

        uploaded = upload_to_gdrive(
            creds=gdrive_creds,
            file_name=file_name,
            file_bytes=file_bytes,
            mime_type=mime_type,
            parent_folder_id=gdrive_folder_id
        )
        migrated.append(uploaded)
    return {
        "files_migrated": len(migrated),
        "details": migrated
    }