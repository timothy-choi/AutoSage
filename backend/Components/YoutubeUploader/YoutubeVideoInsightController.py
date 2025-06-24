from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeVideoInsightHelper import fetch_youtube_video_insights

router = APIRouter()

class YouTubeVideoInsightRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with YouTube read permissions")
    video_id: str = Field(..., description="ID of the YouTube video (e.g., dQw4w9WgXcQ)")

@router.get("/youtube/video-insights")
def get_video_insights(request: YouTubeVideoInsightRequest):
    result = fetch_youtube_video_insights(request.access_token, request.video_id)

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    return result