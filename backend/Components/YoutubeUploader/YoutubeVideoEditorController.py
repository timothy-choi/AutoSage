from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from YoutubeVideoEditorHelper import edit_youtube_video

router = APIRouter()

class YouTubeVideoEditRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with YouTube Data API access")
    video_id: str = Field(..., description="Video ID to edit (e.g., dQw4w9WgXcQ)")
    title: Optional[str] = Field(None, description="New title (optional)")
    description: Optional[str] = Field(None, description="New description (optional)")
    tags: Optional[List[str]] = Field(None, description="New tags list (optional)")
    privacy_status: Optional[str] = Field(None, description="public, private, or unlisted")

@router.put("/youtube/edit-video")
def edit_video(request: YouTubeVideoEditRequest):
    result = edit_youtube_video(
        access_token=request.access_token,
        video_id=request.video_id,
        title=request.title,
        description=request.description,
        tags=request.tags,
        privacy_status=request.privacy_status
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result