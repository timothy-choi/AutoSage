from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from GoogleChatMessageSenderHelper import send_google_chat_message, send_google_chat_card

router = APIRouter()

class ChatMessageRequest(BaseModel):
    webhook_url: str
    text: str

class ChatCardRequest(BaseModel):
    webhook_url: str
    title: str
    subtitle: str
    content: str

@router.post("/google-chat/send-message")
async def send_chat_message(req: ChatMessageRequest):
    result = await send_google_chat_message(req.webhook_url, req.text)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/google-chat/send-card")
async def send_chat_card(req: ChatCardRequest):
    result = await send_google_chat_card(req.webhook_url, req.title, req.subtitle, req.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result