from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarEventEditorHelper import edit_calendar_event

router = APIRouter()

class EventEditRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    calendar_id: str = Field("primary", description="Calendar ID")
    event_id: str = Field(..., description="ID of the event to edit")
    summary: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    timezone: Optional[str] = "UTC"
    location: Optional[str] = None

@router.patch("/gcalendar/edit-event")
def edit_event(request: EventEditRequest):
    try:
        return edit_calendar_event(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            event_id=request.event_id,
            summary=request.summary,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            timezone=request.timezone,
            location=request.location
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))