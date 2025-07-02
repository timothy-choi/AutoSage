from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from NotionToGoogleCalendarSyncerHelper import sync_notion_to_google_calendar

router = APIRouter()

class NotionToGCalRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Notion database ID containing events")
    google_token: str = Field(..., description="Google OAuth 2.0 token with calendar access")
    calendar_id: str = Field(..., description="Google Calendar ID to sync into")
    max_events: int = Field(10, description="Number of Notion entries to sync")

@router.post("/notion/to-google-calendar")
def sync_to_google_calendar(request: NotionToGCalRequest) -> List[dict]:
    try:
        return sync_notion_to_google_calendar(
            notion_token=request.notion_token,
            database_id=request.database_id,
            google_token=request.google_token,
            calendar_id=request.calendar_id,
            max_events=request.max_events
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))