from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from ZoomToSlackBridgeHelper import sync_zoom_meetings_to_slack

router = APIRouter()

class ZoomToSlackRequest(BaseModel):
    user_id: str = Field(..., description="Zoom user ID (e.g. 'me')")
    jwt_token: str = Field(..., description="Zoom JWT token")
    slack_webhook_url: str = Field(..., description="Slack webhook URL to send messages to")
    meeting_type: Literal["upcoming", "past"] = "upcoming"

@router.post("/zoom/sync-to-slack")
def zoom_to_slack(request: ZoomToSlackRequest):
    try:
        result = sync_zoom_meetings_to_slack(
            user_id=request.user_id,
            jwt_token=request.jwt_token,
            slack_webhook_url=request.slack_webhook_url,
            meeting_type=request.meeting_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))