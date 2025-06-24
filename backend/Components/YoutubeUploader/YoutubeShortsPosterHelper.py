from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def post_youtube_shorts_video(
    access_token: str,
    video_path: str,
    title: str,
    description: str = "",
    tags: list[str] = [],
    privacy_status: str = "public"
) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        if "#shorts" not in title.lower():
            title += " #Shorts"
        if "#shorts" not in description.lower():
            description += "\n\n#Shorts"

        body = {
            "snippet": {
                "title": title.strip(),
                "description": description.strip(),
                "tags": tags
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = request.execute()

        return {
            "status": "uploaded",
            "video_id": response.get("id"),
            "link": f"https://youtube.com/shorts/{response.get('id')}"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}