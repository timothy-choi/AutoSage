from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from GoogleChatPollCreatorHelper import send_google_chat_poll

router = APIRouter()

class PollRequest(BaseModel):
    webhook_url: str
    question: str
    options: List[str]

@router.post("/google-chat/create-poll")
async def create_poll(req: PollRequest):
    result = await send_google_chat_poll(req.webhook_url, req.question, req.options)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result