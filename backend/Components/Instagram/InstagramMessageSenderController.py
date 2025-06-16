from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramMessageSenderHelper import send_instagram_dm, send_instagram_media_dm, mark_dm_as_seen

router = APIRouter()

class MessageRequest(BaseModel):
    recipient_id: str
    message: str
    access_token: str

class MediaMessageRequest(BaseModel):
    recipient_id: str
    media_id: str
    access_token: str

class SeenRequest(BaseModel):
    recipient_id: str
    access_token: str

@router.post("/instagram/send-dm")
async def send_dm(req: MessageRequest):
    result = await send_instagram_dm(req.recipient_id, req.message, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/send-media-dm")
async def send_media_dm(req: MediaMessageRequest):
    result = await send_instagram_media_dm(req.recipient_id, req.media_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/mark-dm-seen")
async def mark_seen(req: SeenRequest):
    result = await mark_dm_as_seen(req.recipient_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result