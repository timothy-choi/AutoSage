from fastapi import APIRouter, Query
from ZoomMeetingStarterHelper import get_meeting_start_and_join_info
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")

@router.get("/zoom/meeting/start")
def start_zoom_meeting(
    meeting_id: str = Query(..., description="Zoom Meeting ID")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Zoom API credentials are missing"}

    try:
        result = get_meeting_start_and_join_info(ZOOM_API_KEY, ZOOM_API_SECRET, meeting_id)
        return result
    except Exception as e:
        return {"error": str(e)}