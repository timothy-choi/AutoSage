from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from TwitchKeywordMonitorHelper import set_blocked_keywords, set_allowed_keywords, scan_message

router = APIRouter()

class KeywordUpdateRequest(BaseModel):
    keywords: List[str]

class MessageScanRequest(BaseModel):
    message: str

@router.post("/twitch/monitor/set-blocked")
async def update_blocked_keywords(req: KeywordUpdateRequest):
    set_blocked_keywords(req.keywords)
    return {"status": "blocked keywords updated"}

@router.post("/twitch/monitor/set-allowed")
async def update_allowed_keywords(req: KeywordUpdateRequest):
    set_allowed_keywords(req.keywords)
    return {"status": "allowed keywords updated"}

@router.post("/twitch/monitor/scan")
async def perform_message_scan(req: MessageScanRequest):
    result = scan_message(req.message)
    return result