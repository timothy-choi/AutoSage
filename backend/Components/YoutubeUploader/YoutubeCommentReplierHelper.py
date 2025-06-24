from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def reply_to_youtube_comment(
    access_token: str,
    parent_comment_id: str,
    reply_text: str
) -> dict:
    try:
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        comment_body = {
            "snippet": {
                "parentId": parent_comment_id,
                "textOriginal": reply_text
            }
        }

        response = youtube.comments().insert(
            part="snippet",
            body=comment_body
        ).execute()

        return {
            "status": "replied",
            "reply_id": response.get("id"),
            "message": response["snippet"]["textOriginal"]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}