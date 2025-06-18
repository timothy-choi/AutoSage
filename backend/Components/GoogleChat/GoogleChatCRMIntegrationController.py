from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from GoogleChatCRMIntegrationHelper import (
    send_crm_update_to_googlechat,
    send_crm_lead_alert,
    send_crm_followup_reminder
)

router = APIRouter()

class CRMUpdatePayload(BaseModel):
    lead_name: str
    status: str
    next_step: str = "Not specified"

class GoogleChatCRMRequest(BaseModel):
    webhook_url: str
    crm_data: CRMUpdatePayload

class LeadAlertRequest(BaseModel):
    lead_name: str
    webhook_url: str

class FollowupReminderRequest(BaseModel):
    lead_name: str
    due_date: str
    webhook_url: str

@router.post("/googlechat/crm-update")
async def googlechat_crm_update(req: GoogleChatCRMRequest):
    result = await send_crm_update_to_googlechat(req.crm_data.dict(), req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/googlechat/lead-alert")
async def googlechat_crm_lead_alert(req: LeadAlertRequest):
    result = await send_crm_lead_alert(req.lead_name, req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/googlechat/followup-reminder")
async def googlechat_followup_reminder(req: FollowupReminderRequest):
    result = await send_crm_followup_reminder(req.lead_name, req.due_date, req.webhook_url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result