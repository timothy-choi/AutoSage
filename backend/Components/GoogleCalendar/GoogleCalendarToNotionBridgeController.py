from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarToNotionBridgeHelper import push_calendar_events_to_notion

router = APIRouter()

class CalendarToNotionRequest(BaseModel):
    google_access_token: str = Field(..., description="OAuth token for Google Calendar")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    notion_token: str = Field(..., description="Integration token for Notion")
    notion_database_id: str = Field(..., description="Notion database ID")
    hours_ahead: Optional[int] = Field(24, description="Time window ahead (in hours)")
    max_results: Optional[int] = Field(10, description="Maximum events to sync")

@router.post("/gcalendar/to-notion")
def sync_to_notion(request: CalendarToNotionRequest):
    try:
        return push_calendar_events_to_notion(
            google_access_token=request.google_access_token,
            calendar_id=request.calendar_id,
            notion_token=request.notion_token,
            notion_database_id=request.notion_database_id,
            hours_ahead=request.hours_ahead,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))