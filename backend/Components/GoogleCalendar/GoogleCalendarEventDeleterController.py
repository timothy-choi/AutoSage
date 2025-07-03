from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarEventDeleterHelper import batch_delete_events

router = APIRouter()

class BatchDeleteRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    calendar_id: str = Field("primary", description="Calendar ID")
    time_max: Optional[str] = Field(None, description="Delete events before this ISO 8601 date")
    q: Optional[str] = Field(None, description="Delete events whose summary contains this keyword")

@router.delete("/gcalendar/delete-events")
def batch_delete(request: BatchDeleteRequest):
    try:
        return batch_delete_events(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            time_max=request.time_max,
            q=request.q
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))