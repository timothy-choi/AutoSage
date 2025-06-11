from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TeamsNotificationBridgeHelper import (
    send_teams_notification,
    send_markdown_notification,
    send_notification_with_buttons,
    send_error_alert,
    send_success_alert
)

router = APIRouter()

class TeamsNotificationRequest(BaseModel):
    webhook_url: str
    title: str
    message: str
    color: str = "0076D7"

class MarkdownNotificationRequest(BaseModel):
    webhook_url: str
    markdown: str
    title: str = "Markdown Update"
    color: str = "0076D7"

class ButtonNotificationRequest(BaseModel):
    webhook_url: str
    title: str
    message: str
    buttons: List[dict]  # Each dict must have 'label' and 'url'
    color: str = "0076D7"

class AlertRequest(BaseModel):
    webhook_url: str
    title: str
    message: str

@router.post("/teams/send-notification")
async def send_notification(req: TeamsNotificationRequest):
    result = await send_teams_notification(req.webhook_url, req.title, req.message, req.color)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-markdown")
async def send_markdown(req: MarkdownNotificationRequest):
    result = await send_markdown_notification(req.webhook_url, req.markdown, req.title, req.color)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-buttons")
async def send_buttons(req: ButtonNotificationRequest):
    result = await send_notification_with_buttons(req.webhook_url, req.title, req.message, req.buttons, req.color)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-error-alert")
async def send_error(req: AlertRequest):
    result = await send_error_alert(req.webhook_url, req.title, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-success-alert")
async def send_success(req: AlertRequest):
    result = await send_success_alert(req.webhook_url, req.title, req.message)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result