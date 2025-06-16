from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from TwitchEventReminderHelper import schedule_twitch_event_reminder

router = APIRouter()

class TwitchEventReminderRequest(BaseModel):
    webhook_url: str
    event_name: str
    remind_at: datetime

@router.post("/twitch/schedule-event-reminder")
async def schedule_twitch_event_reminder_endpoint(req: TwitchEventReminderRequest):
    result = await schedule_twitch_event_reminder(req.webhook_url, req.event_name, req.remind_at)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result