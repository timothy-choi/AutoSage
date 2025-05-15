import os
from typing import Optional, List
from google.oauth2 import service_account
from googleapiclient.discovery import build as google_build
from googleapiclient.http import MediaFileUpload
import dropbox
import requests
import json
from msal import PublicClientApplication

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

def list_gdrive_files(folder_id: Optional[str] = None) -> List[str]:
    if not _gdrive_service:
        raise RuntimeError("Google Drive is not configured.")
    query = f"'{folder_id}' in parents" if folder_id else None
    results = _gdrive_service.files().list(q=query, fields="files(id, name)").execute()
    return [f["name"] for f in results.get("files", [])]

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