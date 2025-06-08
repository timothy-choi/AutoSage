from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from DiscordEventReminderHelper import schedule_event_reminder

router = APIRouter()

class EventReminderRequest(BaseModel):
    channel_id: int
    message: str
    remind_at: datetime  

@router.post("/discord/schedule-reminder")
async def schedule_event_reminder_api(req: EventReminderRequest):
    from bot_runner import bot
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot is not ready")

    await schedule_event_reminder(bot, req.channel_id, req.message, req.remind_at)
    return {
        "status": "scheduled",
        "channel_id": req.channel_id,
        "remind_at": req.remind_at.isoformat()
    }