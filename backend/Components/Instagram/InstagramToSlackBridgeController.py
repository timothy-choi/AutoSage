from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramToSlackBridgeHelper import forward_instagram_post_to_slack

router = APIRouter()

class InstagramPostPayload(BaseModel):
    caption: str
    media_url: str
    permalink: str

class SlackBridgeRequest(BaseModel):
    post: InstagramPostPayload
    webhook_url: str

@router.post("/bridge/instagram-to-slack")
async def bridge_instagram_to_slack(req: SlackBridgeRequest):
    result = await forward_instagram_post_to_slack(req.post.dict(), req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result