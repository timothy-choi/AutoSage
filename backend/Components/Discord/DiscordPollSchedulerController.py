from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from DiscordPollSchedulerHelper import schedule_poll

router = APIRouter()

class PollScheduleRequest(BaseModel):
    channel_id: int
    question: str
    options: List[str]
    send_at: datetime  

@router.post("/discord/schedule-poll")
def schedule_discord_poll(req: PollScheduleRequest):
    try:
        schedule_poll(req.channel_id, req.question, req.options, req.send_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "poll scheduled", "channel_id": req.channel_id}