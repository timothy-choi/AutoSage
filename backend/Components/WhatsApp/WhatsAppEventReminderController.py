from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from WhatsAppEventReminderHelper import schedule_reminder

router = APIRouter()

class EventReminderPayload(BaseModel):
    to: str
    message: str
    event_time: str 

@router.post("/whatsapp/event/reminder")
def set_event_reminder(payload: EventReminderPayload):
    try:
        result = schedule_reminder(payload.to, payload.message, payload.event_time)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))