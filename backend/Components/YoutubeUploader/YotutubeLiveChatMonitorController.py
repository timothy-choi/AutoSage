from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from YoutubeLiveChatMonitorHelper import monitor_live_chat_once

router = APIRouter()

class YouTubeLiveChatMonitorRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 access token")
    max_results: Optional[int] = Field(default=10, description="Number of recent messages to return")

@router.post("/youtube/monitor-live-chat")
def monitor_live_chat(request: YouTubeLiveChatMonitorRequest):
    result = monitor_live_chat_once(
        access_token=request.access_token,
        max_results=request.max_results
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result