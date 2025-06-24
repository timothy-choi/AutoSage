from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeChannelStatsCollectorHelper import fetch_youtube_channel_stats

router = APIRouter()

class YouTubeChannelStatsRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with YouTube Data API access")

@router.post("/youtube/channel-stats")
def get_channel_stats(request: YouTubeChannelStatsRequest):
    result = fetch_youtube_channel_stats(request.access_token)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result