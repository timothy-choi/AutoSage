from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def fetch_youtube_channel_stats(access_token: str) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        response = youtube.channels().list(
            part="snippet,statistics",
            mine=True
        ).execute()

        if not response["items"]:
            return {"status": "error", "message": "No channel found for authenticated user."}

        channel = response["items"][0]
        snippet = channel["snippet"]
        stats = channel["statistics"]

        return {
            "status": "success",
            "channel_id": channel["id"],
            "channel_title": snippet.get("title"),
            "description": snippet.get("description"),
            "published_at": snippet.get("publishedAt"),
            "view_count": stats.get("viewCount"),
            "subscriber_count": stats.get("subscriberCount"),
            "video_count": stats.get("videoCount")
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}