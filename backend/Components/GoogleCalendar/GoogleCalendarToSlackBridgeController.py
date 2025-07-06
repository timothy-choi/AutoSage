from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarToSlackBridgeHelper import push_calendar_events_to_slack

router = APIRouter()

class CalendarToSlackRequest(BaseModel):
    access_token: str = Field(..., description="Google OAuth token with calendar access")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    slack_webhook_url: str = Field(..., description="Slack Incoming Webhook URL")
    hours_ahead: Optional[int] = Field(24, description="Time window to look ahead (in hours)")
    max_results: Optional[int] = Field(10, description="Maximum number of events to push")

@router.post("/gcalendar/to-slack")
def calendar_to_slack(request: CalendarToSlackRequest):
    try:
        return push_calendar_events_to_slack(
            access_token=request.access_token,
            calendar_id=request.calendar_id,
            slack_webhook_url=request.slack_webhook_url,
            hours_ahead=request.hours_ahead,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))