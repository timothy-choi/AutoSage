from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarEventFetcherHelper import fetch_calendar_events

router = APIRouter()

class EventFetchRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    calendar_id: Optional[str] = Field("primary", description="Calendar ID")
    time_min: Optional[str] = Field(None, description="ISO start time (inclusive)")
    time_max: Optional[str] = Field(None, description="ISO end time (inclusive)")
    query: Optional[str] = Field(None, description="Text query to filter events")
    max_results: Optional[int] = Field(50, description="Max number of events to return")

@router.post("/gcalendar/fetch-events")
def fetch_events(request: EventFetchRequest):
    try:
        return fetch_calendar_events(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            time_min=request.time_min,
            time_max=request.time_max,
            query=request.query,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))