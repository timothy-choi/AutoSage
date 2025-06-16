from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchStreamAnnouncerHelper import announce_twitch_stream, announce_with_thumbnail

router = APIRouter()

class StreamAnnouncementRequest(BaseModel):
    discord_webhook_url: str
    streamer_name: str
    title: str
    game: str
    url: str

class ThumbnailAnnouncementRequest(StreamAnnouncementRequest):
    thumbnail_url: str

@router.post("/twitch/announce-stream")
async def announce_stream(req: StreamAnnouncementRequest):
    result = await announce_twitch_stream(
        req.discord_webhook_url,
        req.streamer_name,
        req.title,
        req.game,
        req.url
    )
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result

@router.post("/twitch/announce-stream-thumbnail")
async def announce_stream_with_thumbnail(req: ThumbnailAnnouncementRequest):
    result = await announce_with_thumbnail(
        req.discord_webhook_url,
        req.streamer_name,
        req.title,
        req.game,
        req.url,
        req.thumbnail_url
    )
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result