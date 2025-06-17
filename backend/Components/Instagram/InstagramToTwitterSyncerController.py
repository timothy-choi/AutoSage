from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramToTwitterSyncerHelper import sync_instagram_post_to_twitter

router = APIRouter()

class InstagramPostPayload(BaseModel):
    caption: str
    media_url: str
    permalink: str

class TwitterSyncRequest(BaseModel):
    post: InstagramPostPayload
    bearer_token: str

@router.post("/sync/instagram-to-twitter")
async def sync_instagram_to_twitter(req: TwitterSyncRequest):
    result = await sync_instagram_post_to_twitter(req.post.dict(), req.bearer_token)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result