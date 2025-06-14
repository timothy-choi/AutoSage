from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchMessageSenderHelper import send_twitch_chat_message, send_twitch_whisper

router = APIRouter()

class TwitchMessageRequest(BaseModel):
    oauth_token: str
    client_id: str
    broadcaster_id: str
    message: str

class TwitchWhisperRequest(BaseModel):
    oauth_token: str
    client_id: str
    from_user_id: str
    to_user_id: str
    message: str

@router.post("/twitch/send-message")
async def send_twitch_message(req: TwitchMessageRequest):
    result = await send_twitch_chat_message(req.oauth_token, req.client_id, req.broadcaster_id, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/twitch/send-whisper")
async def send_twitch_whisper_message(req: TwitchWhisperRequest):
    result = await send_twitch_whisper(req.oauth_token, req.client_id, req.from_user_id, req.to_user_id, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result