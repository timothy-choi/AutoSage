from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from GoogleChatNotificationBridgeHelper import send_google_chat_notification, send_google_chat_card_notification

router = APIRouter()

class TextNotificationRequest(BaseModel):
    webhook_url: str
    text: str

class CardNotificationRequest(BaseModel):
    webhook_url: str
    title: str
    subtitle: str
    content: str

@router.post("/google-chat/notify")
async def notify_google_chat(req: TextNotificationRequest):
    result = await send_google_chat_notification(req.webhook_url, req.text)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/google-chat/notify-card")
async def notify_google_chat_card(req: CardNotificationRequest):
    result = await send_google_chat_card_notification(req.webhook_url, req.title, req.subtitle, req.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result