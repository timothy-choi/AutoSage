from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def delete_youtube_video(access_token: str, video_id: str) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        youtube.videos().delete(id=video_id).execute()

        return {
            "status": "deleted",
            "video_id": video_id,
            "message": f"Video https://youtu.be/{video_id} has been successfully deleted."
        }
    except Exception as e:
        return {
            "status": "error",
            "video_id": video_id,
            "message": str(e)
        }