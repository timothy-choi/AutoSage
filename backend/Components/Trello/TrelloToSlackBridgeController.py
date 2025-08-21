from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from TrelloToSlackBridgeHelper import send_slack_message, format_trello_event

router = APIRouter()

class SlackBridgeConfig(BaseModel):
    webhook_url: str = Field(..., description="Slack Incoming Webhook URL")

@router.post("/trello/webhook/slack", tags=["Trello to Slack"])
async def trello_to_slack_webhook(
    request: Request,
    config: SlackBridgeConfig
):
    try:
        payload = await request.json()
        message = format_trello_event(payload)
        result = send_slack_message(config.webhook_url, message)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))