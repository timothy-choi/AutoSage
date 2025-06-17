from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramHashtagTrackerHelper import search_hashtag_id, get_hashtag_recent_media

router = APIRouter()

class HashtagSearchRequest(BaseModel):
    hashtag_name: str
    user_id: str
    access_token: str

class HashtagMediaRequest(BaseModel):
    hashtag_id: str
    user_id: str
    access_token: str

@router.post("/instagram/search-hashtag")
async def search_hashtag(req: HashtagSearchRequest):
    result = await search_hashtag_id(req.hashtag_name, req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/hashtag-recent-media")
async def hashtag_recent_media(req: HashtagMediaRequest):
    result = await get_hashtag_recent_media(req.hashtag_id, req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result