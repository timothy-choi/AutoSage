from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def edit_youtube_video(
    access_token: str,
    video_id: str,
    title: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    privacy_status: str | None = None
) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        video_response = youtube.videos().list(
            part="snippet,status",
            id=video_id
        ).execute()

        if not video_response["items"]:
            return {"status": "error", "message": "Video not found or access denied."}

        video = video_response["items"][0]

        snippet = video["snippet"]
        status = video["status"]

        if title: snippet["title"] = title
        if description: snippet["description"] = description
        if tags is not None: snippet["tags"] = tags
        if privacy_status: status["privacyStatus"] = privacy_status

        update_response = youtube.videos().update(
            part="snippet,status",
            body={
                "id": video_id,
                "snippet": snippet,
                "status": status
            }
        ).execute()

        return {
            "status": "updated",
            "video_id": video_id,
            "title": update_response["snippet"]["title"],
            "privacy": update_response["status"]["privacyStatus"]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}