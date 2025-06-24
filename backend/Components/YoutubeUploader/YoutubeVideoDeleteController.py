from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeVideoDeleteHelper import delete_youtube_video

router = APIRouter()

class YouTubeVideoDeleteRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with permission to delete YouTube videos")
    video_id: str = Field(..., description="ID of the YouTube video to delete")

@router.delete("/youtube/delete-video")
def delete_video(request: YouTubeVideoDeleteRequest):
    result = delete_youtube_video(request.access_token, request.video_id)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result