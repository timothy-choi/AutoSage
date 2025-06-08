from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from DiscordMessageSchedulerHelper import schedule_message

router = APIRouter()

class ScheduleRequest(BaseModel):
    channel_id: int
    content: str
    send_at: datetime 

@router.post("/discord/schedule-message")
def schedule_discord_message(req: ScheduleRequest):
    if req.send_at <= datetime.now():
        raise HTTPException(status_code=400, detail="Time must be in the future")
    
    schedule_message(req.channel_id, req.content, req.send_at)
    return {"status": "scheduled", "channel_id": req.channel_id}