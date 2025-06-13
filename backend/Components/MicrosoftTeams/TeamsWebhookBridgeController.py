from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from TeamsWebhookBridgeHelper import (
    send_webhook_message,
    send_webhook_card,
    send_webhook_alert
)

router = APIRouter()

class WebhookMessageRequest(BaseModel):
    webhook_url: str
    title: str
    message: str
    color: str = "0072C6"

class WebhookCardRequest(BaseModel):
    webhook_url: str
    title: str
    facts: List[Dict[str, str]]
    color: str = "0072C6"

class WebhookAlertRequest(BaseModel):
    webhook_url: str
    alert_level: str 
    content: str

@router.post("/teams/send-webhook-message")
async def send_webhook_message_api(req: WebhookMessageRequest):
    result = await send_webhook_message(req.webhook_url, req.title, req.message, req.color)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-webhook-card")
async def send_webhook_card_api(req: WebhookCardRequest):
    result = await send_webhook_card(req.webhook_url, req.title, req.facts, req.color)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-webhook-alert")
async def send_webhook_alert_api(req: WebhookAlertRequest):
    result = await send_webhook_alert(req.webhook_url, req.alert_level, req.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
