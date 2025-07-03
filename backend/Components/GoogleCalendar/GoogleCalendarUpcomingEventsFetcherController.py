from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarUpcomingEventsFetcherHelper import fetch_upcoming_events

router = APIRouter()

class UpcomingEventsRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    calendar_id: Optional[str] = Field("primary", description="Google Calendar ID")
    max_results: Optional[int] = Field(10, description="Max number of upcoming events")
    query: Optional[str] = Field(None, description="Search term to filter events")

@router.post("/gcalendar/fetch-upcoming")
def fetch_upcoming(request: UpcomingEventsRequest):
    try:
        return fetch_upcoming_events(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            max_results=request.max_results,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))