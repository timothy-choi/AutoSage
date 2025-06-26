from fastapi import APIRouter, Query
from typing import Optional
from ZoomMeetingClonerHelper import clone_zoom_meeting
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")
ZOOM_USER_ID = os.getenv("ZOOM_USER_ID", "me")

@router.post("/zoom/meeting/clone")
def clone_meeting(
    original_meeting_id: str = Query(..., description="Zoom meeting ID to clone"),
    new_start_time: Optional[str] = Query(None, description="New start time (ISO format). If not set, uses original time.")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Zoom API credentials missing"}

    try:
        result = clone_zoom_meeting(
            api_key=ZOOM_API_KEY,
            api_secret=ZOOM_API_SECRET,
            user_id=ZOOM_USER_ID,
            original_meeting_id=original_meeting_id,
            new_start_time=new_start_time
        )
        return result
    except Exception as e:
        return {"error": str(e)}