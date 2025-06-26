from fastapi import APIRouter, Query
from typing import Optional
from ZoomRecurringMeetingSchedulerHelper import schedule_recurring_zoom_meeting
import os
import json

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")
ZOOM_USER_ID = os.getenv("ZOOM_USER_ID", "me")

@router.post("/zoom/meeting/schedule-recurring")
def schedule_recurring_meeting(
    topic: str = Query(..., description="Meeting topic"),
    start_time: str = Query(..., description="ISO 8601 start time (e.g. 2025-07-01T15:00:00Z)"),
    duration: int = Query(..., description="Duration in minutes"),
    recurrence_type: int = Query(..., description="1=Daily, 2=Weekly, 3=Monthly"),
    repeat_interval: int = Query(..., description="How often the meeting repeats"),
    end_times: int = Query(..., description="How many times the meeting occurs"),
    timezone: str = Query("UTC", description="Meeting timezone"),
    agenda: str = Query("", description="Meeting agenda"),
    password: Optional[str] = Query(None, description="Optional meeting password")
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Zoom API credentials missing"}

    recurrence = {
        "type": recurrence_type,
        "repeat_interval": repeat_interval,
        "end_times": end_times
    }

    try:
        response = schedule_recurring_zoom_meeting(
            api_key=ZOOM_API_KEY,
            api_secret=ZOOM_API_SECRET,
            user_id=ZOOM_USER_ID,
            topic=topic,
            start_time=start_time,
            duration=duration,
            recurrence=recurrence,
            timezone=timezone,
            agenda=agenda,
            password=password
        )
        return response
    except Exception as e:
        return {"error": str(e)}