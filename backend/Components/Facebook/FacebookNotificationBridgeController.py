from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
from FacebookNotificationBridgeHelper import (
    send_facebook_post_notification,
    send_batch_notifications,
    tag_priority_message,
    handle_webhook_alert
)

router = APIRouter()

class NotificationPayload(BaseModel):
    page_id: str
    message: str
    priority: bool = False

class BatchNotificationPayload(BaseModel):
    page_id: str
    messages: List[str]

class WebhookPayload(BaseModel):
    alert_message: str
    priority: bool = False
    page_id: str

@router.post("/facebook/notify/send")
def send_notification(payload: NotificationPayload):
    try:
        msg = tag_priority_message(payload.message) if payload.priority else payload.message
        result = send_facebook_post_notification(payload.page_id, msg)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/notify/batch")
def send_batch(payload: BatchNotificationPayload):
    try:
        results = send_batch_notifications(payload.page_id, payload.messages)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/notify/webhook")
def receive_webhook(payload: WebhookPayload):
    try:
        result = handle_webhook_alert(payload.dict(), payload.page_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))