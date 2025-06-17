from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramMediaDownloaderHelper import download_instagram_media, get_user_media_list, get_media_insights

router = APIRouter()

class MediaDownloadRequest(BaseModel):
    media_id: str
    access_token: str

class UserMediaRequest(BaseModel):
    user_id: str
    access_token: str

class MediaInsightsRequest(BaseModel):
    media_id: str
    metric: str
    access_token: str

@router.post("/instagram/download-media")
async def download_media(req: MediaDownloadRequest):
    result = await download_instagram_media(req.media_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/user-media")
async def user_media(req: UserMediaRequest):
    result = await get_user_media_list(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/media-insights")
async def media_insights(req: MediaInsightsRequest):
    result = await get_media_insights(req.media_id, req.metric, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result