from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeToTwitterBridgeHelper import sync_youtube_to_twitter

router = APIRouter()

class YouTubeToTwitterRequest(BaseModel):
    api_key: str = Field(..., description="YouTube Data API key")
    channel_id: str = Field(..., description="YouTube channel ID")
    twitter_token: str = Field(..., description="Twitter Bearer token")
    published_within_minutes: int = Field(default=60, description="Lookback window in minutes")

@router.post("/youtube/sync-to-twitter")
def youtube_to_twitter(request: YouTubeToTwitterRequest):
    try:
        result = sync_youtube_to_twitter(
            api_key=request.api_key,
            channel_id=request.channel_id,
            twitter_token=request.twitter_token,
            published_within_minutes=request.published_within_minutes
        )
        return {"posted": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))