from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarEventClonerHelper import clone_event

router = APIRouter()

class EventCloneRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    calendar_id: str = Field("primary", description="Source calendar ID")
    event_id: str = Field(..., description="ID of the event to clone")
    new_start: Optional[str] = Field(None, description="New start time (ISO 8601)")
    new_end: Optional[str] = Field(None, description="New end time (ISO 8601)")
    target_calendar_id: Optional[str] = Field(None, description="Target calendar ID (default: same as source)")

@router.post("/gcalendar/clone-event")
def clone_event_endpoint(request: EventCloneRequest):
    try:
        return clone_event(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            event_id=request.event_id,
            new_start=request.new_start,
            new_end=request.new_end,
            target_calendar_id=request.target_calendar_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))