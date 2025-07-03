from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarEventCreatorHelper import create_calendar_event

router = APIRouter()

class EventRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar scope")
    calendar_id: str = Field("primary", description="Calendar ID (default: primary)")
    summary: str = Field(..., description="Event title")
    description: str = Field(..., description="Event description")
    start_time: str = Field(..., description="Start datetime in ISO 8601 (e.g., 2024-06-30T09:00:00Z)")
    end_time: str = Field(..., description="End datetime in ISO 8601 (e.g., 2024-06-30T10:00:00Z)")
    timezone: Optional[str] = Field("UTC", description="Timezone (default: UTC)")
    location: Optional[str] = Field(None, description="Event location")

@router.post("/gcalendar/create-event")
def create_event(request: EventRequest):
    try:
        return create_calendar_event(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            summary=request.summary,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            timezone=request.timezone,
            location=request.location
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))