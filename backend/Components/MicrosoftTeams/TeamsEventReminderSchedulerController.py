from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from TeamsEventReminderSchedulerHelper import schedule_event_reminder

router = APIRouter()

class TeamsEventReminderRequest(BaseModel):
    webhook_url: str
    message: str
    remind_at: datetime

@router.post("/teams/schedule-reminder")
async def schedule_teams_event_reminder(req: TeamsEventReminderRequest):
    if req.remind_at <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reminder time must be in the future")

    await schedule_event_reminder(req.webhook_url, req.message, req.remind_at)
    return {
        "status": "scheduled",
        "remind_at": req.remind_at.isoformat(),
        "message": req.message
    }