from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TwitchSummaryGeneratorHelper import generate_twitch_summary, generate_detailed_summary

router = APIRouter()

class ClipInfo(BaseModel):
    title: str
    url: str

class StreamSummaryRequest(BaseModel):
    discord_webhook_url: str
    streamer_name: str
    stream_title: str
    viewers: int
    clips: List[ClipInfo]

class DetailedStreamSummaryRequest(BaseModel):
    discord_webhook_url: str
    streamer_name: str
    stream_title: str
    game: str
    duration_seconds: int
    viewers: int
    followers_gained: int
    clips: List[ClipInfo]

@router.post("/twitch/stream-summary")
async def stream_summary(req: StreamSummaryRequest):
    result = await generate_twitch_summary(
        req.discord_webhook_url,
        req.streamer_name,
        req.stream_title,
        req.viewers,
        [clip.dict() for clip in req.clips]
    )
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result

@router.post("/twitch/detailed-stream-summary")
async def detailed_summary(req: DetailedStreamSummaryRequest):
    result = await generate_detailed_summary(
        req.discord_webhook_url,
        req.streamer_name,
        req.stream_title,
        req.game,
        req.duration_seconds,
        req.viewers,
        req.followers_gained,
        [clip.model_dump for clip in req.clips]
    )
    if "error" in result["status"]:
        raise HTTPException(status_code=400, detail=result["status"])
    return result