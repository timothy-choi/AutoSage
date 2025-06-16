from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TwitchModeratorNotifierHelper import (
    notify_twitch_moderators,
    notify_with_username,
    notify_urgent
)

router = APIRouter()

class ModeratorNotificationRequest(BaseModel):
    webhook_urls: List[str]
    message: str

class UsernameAlertRequest(BaseModel):
    webhook_urls: List[str]
    username: str
    issue: str

@router.post("/twitch/notify-moderators")
async def notify_moderators(req: ModeratorNotificationRequest):
    result = await notify_twitch_moderators(req.webhook_urls, req.message)
    if not any(r["ok"] for r in result):
        raise HTTPException(status_code=400, detail="Failed to notify any moderators")
    return {"results": result}

@router.post("/twitch/notify-moderators-username")
async def notify_moderators_with_username(req: UsernameAlertRequest):
    result = await notify_with_username(req.webhook_urls, req.username, req.issue)
    if not any(r["ok"] for r in result):
        raise HTTPException(status_code=400, detail="Failed to notify any moderators")
    return {"results": result}

@router.post("/twitch/notify-moderators-urgent")
async def notify_urgent_moderators(req: ModeratorNotificationRequest):
    result = await notify_urgent(req.webhook_urls, req.message)
    if not any(r["ok"] for r in result):
        raise HTTPException(status_code=400, detail="Failed to notify any moderators")
    return {"results": result}