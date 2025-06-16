from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchToDiscordBridgeHelper import (
    forward_twitch_event_to_discord,
    forward_stream_start_to_discord,
    forward_clip_to_discord
)

router = APIRouter()

class TwitchToDiscordRequest(BaseModel):
    discord_webhook_url: str
    twitch_event: dict

class StreamStartRequest(BaseModel):
    discord_webhook_url: str
    streamer_name: str
    stream_title: str
    stream_url: str

class ClipForwardRequest(BaseModel):
    discord_webhook_url: str
    clip_title: str
    clip_url: str
    creator: str

@router.post("/twitch/bridge-to-discord")
async def bridge_twitch_event_to_discord(req: TwitchToDiscordRequest):
    result = await forward_twitch_event_to_discord(req.discord_webhook_url, req.twitch_event)
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result

@router.post("/twitch/stream-start-to-discord")
async def bridge_stream_start(req: StreamStartRequest):
    result = await forward_stream_start_to_discord(req.discord_webhook_url, req.streamer_name, req.stream_title, req.stream_url)
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result

@router.post("/twitch/clip-to-discord")
async def bridge_clip_to_discord(req: ClipForwardRequest):
    result = await forward_clip_to_discord(req.discord_webhook_url, req.clip_title, req.clip_url, req.creator)
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result