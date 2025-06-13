from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsModeratorToolsHelper import post_warning, post_ban_notice

router = APIRouter()

class WarningRequest(BaseModel):
    webhook_url: str
    user: str
    reason: str

class BanNoticeRequest(BaseModel):
    webhook_url: str
    user: str
    duration: str
    reason: str

@router.post("/teams/moderator/warn")
async def send_warning(req: WarningRequest):
    result = await post_warning(req.webhook_url, req.user, req.reason)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/moderator/ban")
async def send_ban_notice(req: BanNoticeRequest):
    result = await post_ban_notice(req.webhook_url, req.user, req.duration, req.reason)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result