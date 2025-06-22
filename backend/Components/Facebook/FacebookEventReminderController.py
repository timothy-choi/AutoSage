from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from FacebookEventReminderHelper import (
    schedule_event_reminder,
    send_event_reminder_now
)

router = APIRouter()

class ReminderPayload(BaseModel):
    post_id: str
    message: str
    send_at: datetime

class ImmediateReminderPayload(BaseModel):
    post_id: str
    message: str

@router.post("/facebook/event/reminder/schedule")
def schedule_reminder(payload: ReminderPayload):
    try:
        result = schedule_event_reminder(payload.post_id, payload.message, payload.send_at)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/event/reminder/send-now")
def send_reminder_now(payload: ImmediateReminderPayload):
    try:
        comment_id = send_event_reminder_now(payload.post_id, payload.message)
        return {"status": "sent", "comment_id": comment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))