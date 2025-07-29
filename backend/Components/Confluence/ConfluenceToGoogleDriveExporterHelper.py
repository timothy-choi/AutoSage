import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from config import CONFLUENCE_API_BASE, CONFLUENCE_API_HEADERS, get_google_drive_service

def fetch_confluence_page_html(page_id: str) -> dict:
    """
    Fetch the Confluence page title and HTML content.
    """
    url = f"{CONFLUENCE_API_BASE}/content/{page_id}?expand=body.export_view,title"
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    data = response.json()
    return {
        "title": data["title"],
        "html": data["body"]["export_view"]["value"]
    }

def upload_html_to_gdrive(title: str, html_content: str, folder_id: str = None) -> dict:
    """
    Upload the HTML content to Google Drive as a document.
    """
    service = get_google_drive_service()

    media = MediaInMemoryUpload(html_content.encode("utf-8"), mimetype="text/html")
    file_metadata = {
        "name": f"{title}.html",
        "mimeType": "application/vnd.google-apps.document"
    }
    if folder_id:
        file_metadata["parents"] = [folder_id]

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, webViewLink"
    ).execute()
    
    return file

def export_confluence_page_to_gdrive(page_id: str, folder_id: str = None) -> dict:
    try:
        data = fetch_confluence_page_html(page_id)
        uploaded = upload_html_to_gdrive(data["title"], data["html"], folder_id)
        return {"success": True, "file": uploaded}
    except Exception as e:
        return {"success": False, "error": str(e)}