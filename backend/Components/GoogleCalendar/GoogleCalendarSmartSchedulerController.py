from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarSmartSchedulerHelper import smart_schedule_event

router = APIRouter()

class SmartScheduleRequest(BaseModel):
    access_token: str = Field(..., description="Google OAuth token")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    duration_minutes: int = Field(..., description="Meeting duration in minutes")
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Location")
    earliest_start_utc: Optional[str] = Field(None, description="ISO UTC earliest start")
    latest_end_utc: Optional[str] = Field(None, description="ISO UTC latest end")

@router.post("/gcalendar/smart-schedule")
def schedule_smart_event(request: SmartScheduleRequest):
    try:
        return smart_schedule_event(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            duration_minutes=request.duration_minutes,
            title=request.title,
            description=request.description,
            location=request.location,
            earliest_start_utc=request.earliest_start_utc,
            latest_end_utc=request.latest_end_utc
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))