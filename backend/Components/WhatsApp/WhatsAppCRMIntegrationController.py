from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from WhatsAppCRMIntegrationHelper import (
    update_crm_entry,
    get_crm_contact_summary,
    list_crm_contacts
)

router = APIRouter()

class CRMUpdatePayload(BaseModel):
    from_number: str
    message: str
    direction: Optional[str] = "inbound" 

@router.post("/whatsapp/crm/update")
def update_crm(payload: CRMUpdatePayload):
    try:
        update_crm_entry(payload.from_number, payload.message, payload.direction)
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whatsapp/crm/contact/{number}")
def get_contact(number: str):
    try:
        result = get_crm_contact_summary(number)
        return result or {"message": "No CRM data found for this number"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whatsapp/crm/list")
def list_contacts(limit: int = 10):
    try:
        return list_crm_contacts(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))