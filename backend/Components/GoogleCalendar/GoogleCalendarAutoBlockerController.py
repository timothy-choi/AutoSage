from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarAutoBlockerHelper import auto_block_time

router = APIRouter()

class AutoBlockRequest(BaseModel):
    access_token: str = Field(..., description="Google OAuth token")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    duration_minutes: int = Field(..., description="Minutes to block")
    title: Optional[str] = Field(None, description="Title of the event")
    description: Optional[str] = Field(None, description="Optional description")
    start_from: Optional[str] = Field(None, description="ISO UTC start search time")
    end_by: Optional[str] = Field(None, description="ISO UTC end search time")

@router.post("/gcalendar/auto-block")
def auto_block(request: AutoBlockRequest):
    try:
        return auto_block_time(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            duration_minutes=request.duration_minutes,
            title=request.title,
            description=request.description,
            start_from=request.start_from,
            end_by=request.end_by
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))