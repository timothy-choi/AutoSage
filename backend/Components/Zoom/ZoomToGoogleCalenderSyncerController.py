from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from ZoomToGoogleCalendarSyncerHelper import sync_zoom_to_google_calendar

router = APIRouter()

class ZoomGoogleSyncRequest(BaseModel):
    user_id: str = Field(..., description="Zoom user ID (e.g., 'me')")
    zoom_jwt_token: str = Field(..., description="Zoom JWT token")
    google_token: str = Field(..., description="OAuth access token for Google Calendar")
    calendar_id: str = Field(..., description="Google Calendar ID (e.g. 'primary')")
    timezone: str = Field(default="UTC", description="Time zone for calendar events")

@router.post("/zoom/sync-to-google-calendar")
def sync_zoom_to_google_calendar_endpoint(request: ZoomGoogleSyncRequest):
    try:
        results = sync_zoom_to_google_calendar(
            user_id=request.user_id,
            jwt_token=request.zoom_jwt_token,
            calendar_id=request.calendar_id,
            google_token=request.google_token,
            timezone=request.timezone
        )
        return {"synced_events": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))