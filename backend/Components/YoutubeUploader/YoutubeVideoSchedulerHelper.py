import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_youtube_video(
    access_token: str,
    video_path: str,
    title: str,
    description: str,
    privacy_status: str = "private",
    tags: list[str] = []
) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()

        return {
            "status": "uploaded",
            "video_id": response.get("id"),
            "video_link": f"https://youtu.be/{response.get('id')}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def schedule_youtube_upload(
    access_token: str,
    video_path: str,
    title: str,
    description: str,
    scheduled_unix_time: int,
    privacy_status: str = "private",
    tags: list[str] = []
):
    now = int(time.time())
    delay = scheduled_unix_time - now
    if delay > 0:
        time.sleep(delay)

    return upload_youtube_video(access_token, video_path, title, description, privacy_status, tags)