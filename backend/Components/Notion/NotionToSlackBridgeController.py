from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionToSlackBridgeHelper import bridge_notion_to_slack

router = APIRouter()

class NotionSlackBridgeRequest(BaseModel):
    slack_webhook_url: str = Field(..., description="Slack Incoming Webhook URL")
    event: Dict = Field(..., description="Event payload with Notion page info")

@router.post("/notion/to-slack")
def notion_to_slack_bridge(request: NotionSlackBridgeRequest):
    try:
        result = bridge_notion_to_slack(
            slack_webhook_url=request.slack_webhook_url,
            event=request.event
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))