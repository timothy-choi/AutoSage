from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from GoogleCalendarAttendeeAvailabilityCheckerHelper import check_attendee_availability

router = APIRouter()

class AttendeeAvailabilityRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar access")
    attendee_emails: List[str] = Field(..., description="List of attendee email/calendar IDs")
    time_min: str = Field(..., description="Start time (ISO 8601)")
    time_max: str = Field(..., description="End time (ISO 8601)")

@router.post("/gcalendar/check-attendee-availability")
def check_attendee_availability_endpoint(request: AttendeeAvailabilityRequest):
    try:
        return check_attendee_availability(
            access_token=request.access_token,
            attendee_emails=request.attendee_emails,
            time_min=request.time_min,
            time_max=request.time_max
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))