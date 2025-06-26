from fastapi import APIRouter, Query
from ZoomMeetingEditorHelper import update_zoom_meeting
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")

@router.patch("/zoom/meeting/edit")
def edit_meeting(
    meeting_id: str = Query(..., description="Zoom meeting ID to edit"),
    topic: str = Query(None, description="New meeting topic"),
    start_time: str = Query(None, description="New start time (ISO format)"),
    duration: int = Query(None, description="New duration in minutes"),
    timezone: str = Query(None, description="New timezone"),
    agenda: str = Query(None, description="New agenda"),
    password: str = Query(None, description="New password")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Missing Zoom API credentials"}

    try:
        result = update_zoom_meeting(
            api_key=ZOOM_API_KEY,
            api_secret=ZOOM_API_SECRET,
            meeting_id=meeting_id,
            topic=topic,
            start_time=start_time,
            duration=duration,
            timezone=timezone,
            agenda=agenda,
            password=password
        )
        return result
    except Exception as e:
        return {"error": str(e)}