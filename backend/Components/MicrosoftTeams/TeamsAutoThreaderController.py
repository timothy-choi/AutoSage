from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsAutoThreaderHelper import (
    auto_thread_message,
    start_new_thread,
    auto_thread_with_timestamp
)

router = APIRouter()

class ThreadedMessageRequest(BaseModel):
    webhook_url: str
    message: str
    thread_context_url: str = None

class NewThreadRequest(BaseModel):
    webhook_url: str
    title: str
    message: str

class TimestampedMessageRequest(BaseModel):
    webhook_url: str
    message: str

@router.post("/teams/thread-message")
async def send_threaded_message(req: ThreadedMessageRequest):
    result = await auto_thread_message(req.webhook_url, req.message, req.thread_context_url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/start-thread")
async def start_thread(req: NewThreadRequest):
    result = await start_new_thread(req.webhook_url, req.title, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/thread-message-timestamped")
async def send_timestamped_thread_message(req: TimestampedMessageRequest):
    result = await auto_thread_with_timestamp(req.webhook_url, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result