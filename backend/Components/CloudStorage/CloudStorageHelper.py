import os
from typing import Optional, List
from google.oauth2 import service_account
from googleapiclient.discovery import build as google_build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import dropbox
import requests
import json
from msal import PublicClientApplication
import shutil

_gdrive_service = None
_dropbox_client = None
_onedrive_access_token = None

def configure_google_drive(credentials_path: str):
    global _gdrive_service
    scopes = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
    _gdrive_service = google_build('drive', 'v3', credentials=creds)

def configure_dropbox(token: str):
    global _dropbox_client
    _dropbox_client = dropbox.Dropbox(token)

def configure_onedrive(client_id: str, tenant_id: str, scopes: Optional[List[str]] = None):
    global _onedrive_access_token
    app = PublicClientApplication(client_id=client_id, authority=f"https://login.microsoftonline.com/{tenant_id}")
    scopes = scopes or ["Files.ReadWrite"]
    result = app.acquire_token_interactive(scopes=scopes)
    _onedrive_access_token = result.get("access_token")

def upload_to_gdrive(file_path: str, folder_id: Optional[str] = None) -> str:
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    file = _gdrive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def check_gdrive_file_exists(file_id: str) -> bool:
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    try:
        _gdrive_service.files().get(fileId=file_id).execute()
        return True
    except Exception as e:
        if 'notFound' in str(e):
            return False
        raise

def list_gdrive_files(folder_id: Optional[str] = None) -> List[str]:
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    query = f"'{folder_id}' in parents" if folder_id else None
    results = _gdrive_service.files().list(q=query, fields="files(id, name)").execute()
    return [f["name"] for f in results.get("files", [])]

def download_gdrive_file(file_id: str, dest_path: str) -> str:
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    request = _gdrive_service.files().get_media(fileId=file_id)
    with open(dest_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return dest_path

def delete_gdrive_file(file_id: str):
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    _gdrive_service.files().delete(fileId=file_id).execute()

def upload_to_dropbox(file_path: str, dropbox_path: str) -> str:
    if not _dropbox_client:
        raise RuntimeError("Dropbox is not configured.")
    with open(file_path, 'rb') as f:
        _dropbox_client.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    return dropbox_path

def list_dropbox_files(folder_path: str = "") -> List[str]:
    if not _dropbox_client:
        raise RuntimeError("Dropbox is not configured.")
    res = _dropbox_client.files_list_folder(folder_path)
    return [entry.name for entry in res.entries]

def check_dropbox_file_exists(file_path: str) -> bool:
    if not _dropbox_client:
        raise RuntimeError("Dropbox is not configured.")
    try:
        _dropbox_client.files_get_metadata(file_path)
        return True
    except dropbox.exceptions.ApiError as e:
        if isinstance(e.error, dropbox.files.LookupError):
            return False
        raise

def download_dropbox_file(dropbox_path: str, dest_path: str) -> str:
    if not _dropbox_client:
        raise RuntimeError("Dropbox is not configured.")
    with open(dest_path, "wb") as f:
        metadata, res = _dropbox_client.files_download(dropbox_path)
        f.write(res.content)
    return dest_path

def delete_dropbox_file(path: str):
    if not _dropbox_client:
        raise RuntimeError("Dropbox is not configured.")
    _dropbox_client.files_delete_v2(path)

def upload_to_onedrive(file_path: str, remote_name: Optional[str] = None) -> str:
    if not _onedrive_access_token:
        raise RuntimeError("OneDrive is not configured.")
    headers = {
        "Authorization": f"Bearer {_onedrive_access_token}",
        "Content-Type": "application/octet-stream"
    }
    remote_name = remote_name or os.path.basename(file_path)
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{remote_name}:/content"
    with open(file_path, 'rb') as f:
        response = requests.put(url, headers=headers, data=f.read())
    if response.status_code in (200, 201):
        return response.json().get("id")
    else:
        raise RuntimeError(f"OneDrive upload failed: {response.status_code} {response.text}")

def list_onedrive_files() -> List[str]:
    if not _onedrive_access_token:
        raise RuntimeError("OneDrive is not configured.")
    headers = {"Authorization": f"Bearer {_onedrive_access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [item["name"] for item in data.get("value", [])]
    else:
        raise RuntimeError(f"OneDrive list failed: {response.status_code} {response.text}")
    
def check_if_onedrive_file_exists(filename: str) -> bool:
    if not _onedrive_access_token:
        raise RuntimeError("OneDrive is not configured.")
    headers = {"Authorization": f"Bearer {_onedrive_access_token}"}
    url = f"https://graph.microsoft.com/v1.0/me/drive/root/children?$filter=name eq '{filename}'"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get("value", [])
        return any(item.get("name") == filename for item in items)
    else:
        raise RuntimeError(f"OneDrive existence check failed: {response.status_code} {response.text}")

    
def download_onedrive_file(file_id: str, dest_path: str) -> str:
    if not _onedrive_access_token:
        raise RuntimeError("OneDrive is not configured.")
    headers = {"Authorization": f"Bearer {_onedrive_access_token}"}
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return dest_path
    else:
        raise RuntimeError(f"OneDrive download failed: {response.status_code} {response.text}")

def delete_onedrive_file(item_id: str):
    if not _onedrive_access_token:
        raise RuntimeError("OneDrive is not configured.")
    headers = {"Authorization": f"Bearer {_onedrive_access_token}"}
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code not in (204, 202):
        raise RuntimeError(f"OneDrive delete failed: {response.status_code} {response.text}")
    
def push_backup_to_cloud(backup_path: str, provider: str, folder_id: str, remote_name: str) -> str:
    filename = os.path.basename(backup_path)
    if os.path.isdir(backup_path):
        archive_name = shutil.make_archive(backup_path, 'zip', backup_path)
        backup_path = archive_name
        filename = os.path.basename(archive_name)

    cloud_path = f"/backups/{filename}"

    if provider == "dropbox":
        return upload_to_dropbox(backup_path, cloud_path)
    elif provider == "onedrive":
        return upload_to_onedrive(backup_path, remote_name)
    elif provider == "gdrive":
        return upload_to_gdrive(backup_path, folder_id)
    else:
        raise ValueError(f"Unsupported cloud provider: {provider}")