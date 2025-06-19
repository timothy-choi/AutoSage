from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from WhatsAppNotificationBridgeHelper import (
    send_whatsapp_notification,
    send_batch_notifications,
    get_notification_history,
    retry_failed_notifications,
    handle_webhook_notification
)

router = APIRouter()

class NotificationPayload(BaseModel):
    to: str
    subject: str
    content: str
    level: str = "INFO"

class BatchNotificationPayload(BaseModel):
    recipients: List[str]
    subject: str
    content: str

@router.post("/whatsapp/notify")
def notify(payload: NotificationPayload):
    try:
        sid = send_whatsapp_notification(payload.to, payload.subject, payload.content, payload.level)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/notify/batch")
def notify_batch(payload: BatchNotificationPayload):
    try:
        results = send_batch_notifications(payload.recipients, payload.subject, payload.content)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/whatsapp/notify/history")
def get_history(limit: int = 10):
    try:
        history = get_notification_history(limit)
        return {"notifications": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/notify/retry")
def retry_failed():
    try:
        results = retry_failed_notifications()
        return {"retried": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/notify/webhook")
async def webhook_notification(request: Request):
    try:
        payload = await request.json()
        sid = handle_webhook_notification(payload)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))