from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from GoogleChatThreadReplierHelper import reply_in_google_chat_thread, reply_with_card_in_thread

router = APIRouter()

class ThreadReplyRequest(BaseModel):
    space_name: str
    thread_name: str
    access_token: str
    message: str

class ThreadCardReplyRequest(BaseModel):
    space_name: str
    thread_name: str
    access_token: str
    title: str
    content: str

@router.post("/google-chat/reply-thread")
async def reply_to_thread(req: ThreadReplyRequest):
    result = await reply_in_google_chat_thread(req.space_name, req.thread_name, req.access_token, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/google-chat/reply-thread-card")
async def reply_to_thread_with_card(req: ThreadCardReplyRequest):
    result = await reply_with_card_in_thread(req.space_name, req.thread_name, req.access_token, req.title, req.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result