from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from TeamsMeetingNotifierHelper import schedule_meeting_notification

router = APIRouter()

class TeamsMeetingNotificationRequest(BaseModel):
    webhook_url: str
    meeting_title: str
    start_time: datetime

@router.post("/teams/schedule-meeting-notification")
async def schedule_teams_meeting_notification(req: TeamsMeetingNotificationRequest):
    if req.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Start time must be in the future")

    await schedule_meeting_notification(req.webhook_url, req.meeting_title, req.start_time)
    return {
        "status": "scheduled",
        "notify_at": (req.start_time - timedelta(minutes=5)).isoformat(),
        "meeting_title": req.meeting_title
    }