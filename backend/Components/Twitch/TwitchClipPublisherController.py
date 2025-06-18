from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchClipPublisherHelper import publish_twitch_clip, get_clip_status

router = APIRouter()

class ClipPublishRequest(BaseModel):
    broadcaster_id: str
    oauth_token: str
    client_id: str

class ClipStatusRequest(BaseModel):
    clip_id: str
    oauth_token: str
    client_id: str

@router.post("/twitch/publish-clip")
async def twitch_publish_clip(req: ClipPublishRequest):
    result = await publish_twitch_clip(req.broadcaster_id, req.oauth_token, req.client_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/twitch/clip-status")
async def twitch_clip_status(req: ClipStatusRequest):
    result = await get_clip_status(req.clip_id, req.oauth_token, req.client_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result