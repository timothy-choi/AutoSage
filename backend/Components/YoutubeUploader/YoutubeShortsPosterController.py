from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from YoutubeShortsPosterHelper import post_youtube_shorts_video

router = APIRouter()

class YouTubeShortsRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with YouTube upload permissions")
    video_path: str = Field(..., description="Local path to .mp4 file (≤ 60 seconds, vertical)")
    title: str = Field(..., description="Title of the Shorts video")
    description: Optional[str] = Field(default="", description="Video description")
    tags: Optional[List[str]] = Field(default_factory=list)
    privacy_status: str = Field(default="public", description="public | private | unlisted")

@router.post("/youtube/post-shorts")
def upload_shorts_video(request: YouTubeShortsRequest):
    result = post_youtube_shorts_video(
        access_token=request.access_token,
        video_path=request.video_path,
        title=request.title,
        description=request.description,
        tags=request.tags,
        privacy_status=request.privacy_status
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result