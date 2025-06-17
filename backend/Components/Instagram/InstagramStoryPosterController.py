from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramStoryPosterHelper import post_instagram_story, post_video_story

router = APIRouter()

class StoryPostRequest(BaseModel):
    image_url: str
    access_token: str
    instagram_account_id: str

class VideoStoryRequest(BaseModel):
    video_url: str
    access_token: str
    instagram_account_id: str

@router.post("/instagram/post-story")
async def post_story(req: StoryPostRequest):
    result = await post_instagram_story(req.image_url, req.access_token, req.instagram_account_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/post-video-story")
async def post_video(req: VideoStoryRequest):
    result = await post_video_story(req.video_url, req.access_token, req.instagram_account_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result