from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarMeetingLoadAnalyzerHelper import analyze_meeting_load

router = APIRouter()

class MeetingLoadRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar access")
    calendar_id: str = Field("primary", description="Calendar ID")
    time_min: str = Field(..., description="ISO 8601 start of analysis window")
    time_max: str = Field(..., description="ISO 8601 end of analysis window")
    max_results: Optional[int] = Field(2500, description="Max number of events to fetch")

@router.post("/gcalendar/analyze-meeting-load")
def analyze_load(request: MeetingLoadRequest):
    try:
        return analyze_meeting_load(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            time_min=request.time_min,
            time_max=request.time_max,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))