from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from GoogleCalendarFreeBusyCheckerHelper import check_free_busy

router = APIRouter()

class FreeBusyRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    time_min: str = Field(..., description="Start time (ISO 8601)")
    time_max: str = Field(..., description="End time (ISO 8601)")
    calendar_ids: List[str] = Field(..., description="List of calendar IDs to check")

@router.post("/gcalendar/check-free-busy")
def check_availability(request: FreeBusyRequest):
    try:
        return check_free_busy(
            access_token=request.access_token,
            time_min=request.time_min,
            time_max=request.time_max,
            calendar_ids=request.calendar_ids
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))