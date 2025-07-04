from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarDailyAgendaSenderHelper import fetch_daily_agenda

router = APIRouter()

class DailyAgendaRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar scope")
    calendar_id: Optional[str] = Field("primary", description="Google Calendar ID")
    timezone: Optional[str] = Field("UTC", description="Timezone for today")
    max_results: Optional[int] = Field(20, description="Max number of events to include")

@router.post("/gcalendar/send-daily-agenda")
def send_agenda(request: DailyAgendaRequest):
    try:
        return fetch_daily_agenda(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            timezone=request.timezone,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))