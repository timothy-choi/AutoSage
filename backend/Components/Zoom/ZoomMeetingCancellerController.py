from fastapi import APIRouter, Query
from ZoomMeetingCancellerHelper import cancel_zoom_meeting
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")

@router.delete("/zoom/meeting/cancel")
def cancel_meeting(
    meeting_id: str = Query(..., description="Zoom Meeting ID to cancel")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Zoom API credentials are missing"}

    try:
        result = cancel_zoom_meeting(ZOOM_API_KEY, ZOOM_API_SECRET, meeting_id)
        return result
    except Exception as e:
        return {"error": str(e)}