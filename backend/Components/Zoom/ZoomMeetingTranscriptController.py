from fastapi import APIRouter, Query
from ZoomMeetingTranscriptSenderHelper import (
    fetch_meeting_recordings,
    get_transcript_file_url,
    download_transcript,
    send_transcript_to_webhook
)
from ZoomMeetingCreatorHelper import get_jwt_token
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")

@router.post("/zoom/meeting/transcript/send")
def send_zoom_transcript(
    meeting_id: str = Query(..., description="Zoom meeting ID"),
    webhook_url: str = Query(..., description="Webhook or endpoint to send the transcript to")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Zoom credentials missing"}

    try:
        recordings = fetch_meeting_recordings(ZOOM_API_KEY, ZOOM_API_SECRET, meeting_id)

        if "error" in recordings:
            return recordings

        download_url = get_transcript_file_url(recordings)

        if not download_url:
            return {"error": "Transcript not available or not completed"}

        token = get_jwt_token(ZOOM_API_KEY, ZOOM_API_SECRET)
        transcript_text = download_transcript(download_url, token)

        if not transcript_text:
            return {"error": "Failed to download transcript"}

        result = send_transcript_to_webhook(transcript_text, webhook_url)
        return {"status": "sent", "webhook_response": result}

    except Exception as e:
        return {"error": str(e)}