from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeToSlackNotifierHelper import notify_youtube_uploads_to_slack

router = APIRouter()

class YouTubeToSlackRequest(BaseModel):
    api_key: str = Field(..., description="YouTube Data API v3 key")
    channel_id: str = Field(..., description="YouTube channel ID")
    slack_webhook_url: str = Field(..., description="Slack webhook URL")
    published_within_minutes: int = Field(default=60, description="Look for videos published in the last X minutes")

@router.post("/youtube/notify-to-slack")
def youtube_to_slack(request: YouTubeToSlackRequest):
    try:
        result = notify_youtube_uploads_to_slack(
            api_key=request.api_key,
            channel_id=request.channel_id,
            slack_webhook_url=request.slack_webhook_url,
            published_within_minutes=request.published_within_minutes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))