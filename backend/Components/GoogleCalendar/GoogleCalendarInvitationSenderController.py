from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleCalendarInvitationSenderHelper import send_calendar_invitation

router = APIRouter()

class InvitationRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar access")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    summary: str = Field(..., description="Event title")
    description: str = Field(..., description="Event description")
    start_time: str = Field(..., description="ISO 8601 start time")
    end_time: str = Field(..., description="ISO 8601 end time")
    timezone: str = Field("UTC", description="Timezone")
    attendees: List[str] = Field(..., description="List of attendee emails")
    location: Optional[str] = Field(None, description="Event location")

@router.post("/gcalendar/send-invite")
def send_invite(request: InvitationRequest):
    try:
        return send_calendar_invitation(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            summary=request.summary,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            timezone=request.timezone,
            attendees=request.attendees,
            location=request.location
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))