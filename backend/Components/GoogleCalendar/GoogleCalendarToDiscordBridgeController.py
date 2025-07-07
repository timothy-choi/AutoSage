from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarToDiscordBridgeHelper import push_calendar_events_to_discord

router = APIRouter()

class CalendarToDiscordRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token for Google Calendar")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    discord_webhook_url: str = Field(..., description="Discord Incoming Webhook URL")
    hours_ahead: Optional[int] = Field(24, description="How far ahead to look (in hours)")
    max_results: Optional[int] = Field(10, description="Maximum number of events")

@router.post("/gcalendar/to-discord")
def send_to_discord(request: CalendarToDiscordRequest):
    try:
        return push_calendar_events_to_discord(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            discord_webhook_url=request.discord_webhook_url,
            hours_ahead=request.hours_ahead,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))