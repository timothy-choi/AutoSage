from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleCalendarRSVPHandlerHelper import handle_rsvp

router = APIRouter()

class RSVPRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar access")
    calendar_id: str = Field("primary", description="Calendar ID")
    event_id: str = Field(..., description="Event ID")
    user_email: str = Field(..., description="Your email in the attendee list")
    response_status: str = Field(..., regex="^(accepted|declined|tentative)$")

@router.post("/gcalendar/rsvp")
def rsvp_to_event(request: RSVPRequest):
    try:
        return handle_rsvp(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            event_id=request.event_id,
            user_email=request.user_email,
            response_status=request.response_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))