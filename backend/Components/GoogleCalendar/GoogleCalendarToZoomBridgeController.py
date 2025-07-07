from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarToZoomBridgeHelper import push_calendar_events_to_zoom

router = APIRouter()

class CalendarToZoomRequest(BaseModel):
    google_access_token: str = Field(..., description="Google Calendar OAuth token")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    zoom_jwt_token: str = Field(..., description="Zoom JWT token")
    hours_ahead: Optional[int] = Field(24, description="Time range in hours")
    max_results: Optional[int] = Field(10, description="Max events to process")

@router.post("/gcalendar/to-zoom")
def calendar_to_zoom(request: CalendarToZoomRequest):
    try:
        return push_calendar_events_to_zoom(
            google_access_token=request.google_access_token,
            calendar_id=request.calendar_id,
            zoom_jwt_token=request.zoom_jwt_token,
            hours_ahead=request.hours_ahead,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))