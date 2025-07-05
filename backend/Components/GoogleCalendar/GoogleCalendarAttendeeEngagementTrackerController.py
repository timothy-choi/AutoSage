from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarAttendeeEngagementTrackerHelper import track_attendee_engagement

router = APIRouter()

class AttendeeEngagementRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar access")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    attendee_email: str = Field(..., description="Email address of attendee to track")
    time_min: str = Field(..., description="Start of analysis window (ISO 8601)")
    time_max: str = Field(..., description="End of analysis window (ISO 8601)")
    max_results: Optional[int] = Field(2500, description="Max number of events to fetch")

@router.post("/gcalendar/track-attendee-engagement")
def track_engagement(request: AttendeeEngagementRequest):
    try:
        return track_attendee_engagement(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            attendee_email=request.attendee_email,
            time_min=request.time_min,
            time_max=request.time_max,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))