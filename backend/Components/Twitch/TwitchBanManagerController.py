from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchBanManagerHelper import ban_user, unban_user

router = APIRouter()

class BanRequest(BaseModel):
    oauth_token: str
    client_id: str
    broadcaster_id: str
    user_id: str
    reason: str

class UnbanRequest(BaseModel):
    oauth_token: str
    client_id: str
    broadcaster_id: str
    user_id: str

@router.post("/twitch/ban")
async def ban(req: BanRequest):
    result = await ban_user(req.oauth_token, req.client_id, req.broadcaster_id, req.user_id, req.reason)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/twitch/unban")
async def unban(req: UnbanRequest):
    result = await unban_user(req.oauth_token, req.client_id, req.broadcaster_id, req.user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result