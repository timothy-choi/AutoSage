from fastapi import APIRouter, Query
from ZoomMeetingCreatorHelper import create_zoom_meeting
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")
ZOOM_USER_ID = os.getenv("ZOOM_USER_ID", "me")  

@router.post("/zoom/meeting/create")
def create_meeting(
    topic: str = Query(..., description="Meeting topic/title"),
    start_time: str = Query(..., description="Start time in ISO format (e.g., 2025-06-30T10:00:00Z)"),
    duration: int = Query(..., description="Duration in minutes"),
    timezone: str = Query("UTC", description="Timezone (default: UTC)"),
    agenda: str = Query("", description="Meeting agenda"),
    password: str = Query(None, description="Optional meeting password")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Missing Zoom API credentials in environment variables"}

    try:
        response = create_zoom_meeting(
            api_key=ZOOM_API_KEY,
            api_secret=ZOOM_API_SECRET,
            user_id=ZOOM_USER_ID,
            topic=topic,
            start_time=start_time,
            duration=duration,
            timezone=timezone,
            agenda=agenda,
            password=password
        )
        return response
    except Exception as e:
        return {"error": str(e)}