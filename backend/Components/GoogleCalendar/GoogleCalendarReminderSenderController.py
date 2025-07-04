from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarReminderSenderHelper import send_manual_reminders

router = APIRouter()

class ReminderRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar scope")
    calendar_id: Optional[str] = Field("primary", description="Calendar ID")
    hours_ahead: Optional[int] = Field(24, description="Lookahead time in hours")
    filter_query: Optional[str] = Field(None, description="Keyword filter")
    max_results: Optional[int] = Field(10, description="Max number of events to process")

@router.post("/gcalendar/send-reminders")
def send_reminders(request: ReminderRequest):
    try:
        return send_manual_reminders(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            hours_ahead=request.hours_ahead,
            filter_query=request.filter_query,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))