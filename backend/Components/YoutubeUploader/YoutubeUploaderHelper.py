import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_youtube(credentials_path: str = "client_secrets.json"):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_console()
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def upload_video_to_youtube(
    file_path: str,
    title: str,
    description: str = "",
    tags: list = None,
    category_id: str = "22",
    privacy_status: str = "unlisted",
    credentials_path: str = "client_secrets.json"
) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video not found: {file_path}")

    youtube = authenticate_youtube(credentials_path)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    return response