from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from TeamsCRMIntegrationHelper import (
    create_crm_contact,
    update_crm_contact,
    fetch_crm_contact
)

router = APIRouter()

class CRMContactRequest(BaseModel):
    api_url: str
    token: str
    name: str
    email: str
    phone: Optional[str] = None

class CRMContactUpdateRequest(BaseModel):
    api_url: str
    token: str
    contact_id: str
    updates: Dict[str, str]

class CRMContactFetchRequest(BaseModel):
    api_url: str
    token: str
    contact_id: str

@router.post("/teams/crm/create-contact")
async def create_contact(req: CRMContactRequest):
    result = await create_crm_contact(req.api_url, req.token, req.name, req.email, req.phone)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.put("/teams/crm/update-contact")
async def update_contact(req: CRMContactUpdateRequest):
    result = await update_crm_contact(req.api_url, req.token, req.contact_id, req.updates)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/teams/crm/fetch-contact")
async def fetch_contact(req: CRMContactFetchRequest):
    result = await fetch_crm_contact(req.api_url, req.token, req.contact_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result