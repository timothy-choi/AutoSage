from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from WhatsAppMessageSenderHelper import (
    send_whatsapp_message,
    send_whatsapp_media_message,
    fetch_whatsapp_message_status,
    list_recent_whatsapp_messages,
    schedule_whatsapp_message,
    process_incoming_message
)

router = APIRouter()

class TextMessagePayload(BaseModel):
    to: str
    message: str

class MediaMessagePayload(BaseModel):
    to: str
    media_url: str
    caption: Optional[str] = ""

class StatusCheckPayload(BaseModel):
    sid: str

class ScheduleMessagePayload(BaseModel):
    to: str
    message: str
    delay_seconds: int

@router.post("/whatsapp/send")
def send_text(payload: TextMessagePayload):
    try:
        sid = send_whatsapp_message(payload.to, payload.message)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/send-media")
def send_media(payload: MediaMessagePayload):
    try:
        sid = send_whatsapp_media_message(payload.to, payload.media_url, payload.caption)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/status")
def check_status(payload: StatusCheckPayload):
    try:
        status = fetch_whatsapp_message_status(payload.sid)
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/whatsapp/recent")
def recent_messages(limit: int = 10):
    try:
        messages = list_recent_whatsapp_messages(limit)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/schedule")
def schedule_message(payload: ScheduleMessagePayload):
    try:
        result = schedule_whatsapp_message(payload.to, payload.message, payload.delay_seconds)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/webhook")
async def receive_webhook(request: Request):
    form_data = await request.form()
    from_number = form_data.get("From", "")
    message_body = form_data.get("Body", "")
    response_text = process_incoming_message(from_number, message_body)
    return {"reply": response_text}