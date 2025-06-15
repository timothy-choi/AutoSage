from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from GoogleChatMessageSchedulerHelper import schedule_google_chat_message, schedule_google_chat_card

router = APIRouter()

class GoogleChatScheduleRequest(BaseModel):
    webhook_url: str
    text: str
    send_at: datetime

class GoogleChatCardScheduleRequest(BaseModel):
    webhook_url: str
    title: str
    subtitle: str
    content: str
    send_at: datetime

@router.post("/google-chat/schedule-message")
async def schedule_google_chat_message_endpoint(req: GoogleChatScheduleRequest):
    result = await schedule_google_chat_message(req.webhook_url, req.text, req.send_at)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/google-chat/schedule-card")
async def schedule_google_chat_card_endpoint(req: GoogleChatCardScheduleRequest):
    result = await schedule_google_chat_card(
        req.webhook_url, req.title, req.subtitle, req.content, req.send_at
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result