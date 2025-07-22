import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload

FIGMA_API_BASE = "https://api.figma.com/v1"

def get_figma_image_urls(figma_token, file_key, node_ids, format="png"):
    headers = {"X-Figma-Token": figma_token}
    url = f"{FIGMA_API_BASE}/images/{file_key}"
    params = {
        "ids": ",".join(node_ids),
        "format": format
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("images", {})

def download_figma_image(image_url):
    resp = requests.get(image_url)
    resp.raise_for_status()
    return BytesIO(resp.content)

def upload_to_google_drive(service_account_json, file_stream, filename, mime_type, folder_id):
    credentials = Credentials.from_service_account_file(service_account_json, scopes=["https://www.googleapis.com/auth/drive.file"])
    drive_service = build('drive', 'v3', credentials=credentials)

    media = MediaIoBaseUpload(file_stream, mimetype=mime_type)
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    return {
        "file_id": uploaded_file["id"],
        "name": uploaded_file["name"],
        "link": uploaded_file["webViewLink"]
    }

def export_figma_to_drive(figma_token, file_key, node_ids, format, service_account_json, folder_id):
    image_urls = get_figma_image_urls(figma_token, file_key, node_ids, format=format)
    results = []

    for node_id, image_url in image_urls.items():
        file_stream = download_figma_image(image_url)
        filename = f"{file_key}_{node_id}.{format}"
        mime_type = "image/png" if format == "png" else "application/pdf"
        upload_result = upload_to_google_drive(service_account_json, file_stream, filename, mime_type, folder_id)
        results.append(upload_result)

    return results