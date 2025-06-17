from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramToDiscordBridgeHelper import (
    forward_instagram_post_to_discord,
    forward_instagram_story_to_discord,
    forward_instagram_reel_to_discord
)

router = APIRouter()

class InstagramPostPayload(BaseModel):
    caption: str
    media_url: str
    permalink: str

class DiscordBridgeRequest(BaseModel):
    post: InstagramPostPayload
    webhook_url: str

class StoryBridgeRequest(BaseModel):
    story_url: str
    webhook_url: str

class ReelBridgeRequest(BaseModel):
    reel_url: str
    caption: str
    webhook_url: str

@router.post("/bridge/instagram-to-discord")
async def bridge_instagram_to_discord(req: DiscordBridgeRequest):
    result = await forward_instagram_post_to_discord(req.post.dict(), req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/bridge/instagram-story-to-discord")
async def bridge_story_to_discord(req: StoryBridgeRequest):
    result = await forward_instagram_story_to_discord(req.story_url, req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/bridge/instagram-reel-to-discord")
async def bridge_reel_to_discord(req: ReelBridgeRequest):
    result = await forward_instagram_reel_to_discord(req.reel_url, req.caption, req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result