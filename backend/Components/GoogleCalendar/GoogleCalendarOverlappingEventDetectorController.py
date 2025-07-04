from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarOverlappingEventDetectorHelper import detect_overlapping_events

router = APIRouter()

class OverlapDetectionRequest(BaseModel):
    access_token: str = Field(..., description="OAuth access token")
    calendar_id: str = Field("primary", description="Calendar ID")
    time_min: str = Field(..., description="Start of time window (ISO 8601)")
    time_max: str = Field(..., description="End of time window (ISO 8601)")
    max_results: Optional[int] = Field(50, description="Max number of events to scan")

@router.post("/gcalendar/detect-overlaps")
def detect_overlaps(request: OverlapDetectionRequest):
    try:
        return detect_overlapping_events(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            time_min=request.time_min,
            time_max=request.time_max,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))