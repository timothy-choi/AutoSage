from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def fetch_youtube_video_insights(access_token: str, video_id: str) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        response = youtube.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=video_id
        ).execute()

        if not response["items"]:
            return {"status": "error", "message": "Video not found or access denied."}

        video = response["items"][0]

        snippet = video["snippet"]
        statistics = video["statistics"]
        content_details = video["contentDetails"]
        status = video["status"]

        return {
            "status": "success",
            "video_id": video_id,
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "tags": snippet.get("tags", []),
            "published_at": snippet.get("publishedAt"),
            "duration": content_details.get("duration"), 
            "privacy_status": status.get("privacyStatus"),
            "views": statistics.get("viewCount"),
            "likes": statistics.get("likeCount"),
            "comments": statistics.get("commentCount")
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}