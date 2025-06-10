from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from TeamsMessageSchedulerHelper import schedule_teams_message

router = APIRouter()

class TeamsMessageScheduleRequest(BaseModel):
    webhook_url: str
    content: str
    send_at: datetime

@router.post("/teams/schedule-message")
async def schedule_teams_message_api(req: TeamsMessageScheduleRequest):
    if req.send_at <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

    await schedule_teams_message(req.webhook_url, req.content, req.send_at)
    return {
        "status": "scheduled",
        "send_at": req.send_at.isoformat(),
        "content": req.content
    }