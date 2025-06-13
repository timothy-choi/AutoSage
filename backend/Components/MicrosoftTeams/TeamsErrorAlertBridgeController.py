from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsErrorAlertBridgeHelper import (
    send_error_alert,
    send_critical_alert,
    send_warning_alert
)

router = APIRouter()

class ErrorAlertRequest(BaseModel):
    webhook_url: str
    error_message: str
    service_name: str = "Unknown Service"

class CriticalAlertRequest(BaseModel):
    webhook_url: str
    message: str
    system_name: str

class WarningAlertRequest(BaseModel):
    webhook_url: str
    message: str
    service_name: str

@router.post("/teams/send-error-alert")
async def send_error_alert_api(req: ErrorAlertRequest):
    result = await send_error_alert(req.webhook_url, req.error_message, req.service_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-critical-alert")
async def send_critical_alert_api(req: CriticalAlertRequest):
    result = await send_critical_alert(req.webhook_url, req.message, req.system_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-warning-alert")
async def send_warning_alert_api(req: WarningAlertRequest):
    result = await send_warning_alert(req.webhook_url, req.message, req.service_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result