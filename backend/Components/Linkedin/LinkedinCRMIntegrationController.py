from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from LinkedinCRMIntegrationHelper import (
    format_crm_payload_from_linkedin,
    send_lead_to_crm_webhook
)

router = APIRouter()

class LinkedInCRMLeadRequest(BaseModel):
    name: str = Field(..., description="Lead name")
    title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    message: Optional[str] = Field(None, description="Message or context")
    webhook_url: str = Field(..., description="CRM webhook to send data to")

@router.post("/linkedin/crm-integration")
def integrate_with_crm(request: LinkedInCRMLeadRequest):
    crm_payload = format_crm_payload_from_linkedin(request.dict(exclude={"webhook_url"}))
    result = send_lead_to_crm_webhook(request.webhook_url, crm_payload)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result