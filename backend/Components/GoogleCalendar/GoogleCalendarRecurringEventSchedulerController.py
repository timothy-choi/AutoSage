from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarRecurringEventSchedulerHelper import create_recurring_event

router = APIRouter()

class RecurringEventRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar scope")
    calendar_id: str = Field("primary", description="Calendar ID (default: primary)")
    summary: str = Field(..., description="Event title")
    description: str = Field(..., description="Event description")
    start_time: str = Field(..., description="Start datetime (ISO 8601)")
    end_time: str = Field(..., description="End datetime (ISO 8601)")
    timezone: str = Field("UTC", description="Timezone")
    rrule: str = Field(..., description="Recurrence rule in RRULE format")
    location: Optional[str] = Field(None, description="Event location")

@router.post("/gcalendar/schedule-recurring")
def schedule_recurring_event(request: RecurringEventRequest):
    try:
        return create_recurring_event(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            summary=request.summary,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            timezone=request.timezone,
            rrule=request.rrule,
            location=request.location
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))