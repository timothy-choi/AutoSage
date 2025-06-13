from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from TeamsAccessRequestHandlerHelper import (
    send_access_request,
    send_bulk_access_requests,
    send_access_request_reminder
)

router = APIRouter()

class AccessRequest(BaseModel):
    webhook_url: str
    requester: str
    resource: str
    justification: str

class BulkAccessRequest(BaseModel):
    webhook_url: str
    requests: List[Dict[str, str]]

class AccessReminderRequest(BaseModel):
    webhook_url: str
    requester: str
    resource: str

@router.post("/teams/send-access-request")
async def send_access_request_api(req: AccessRequest):
    result = await send_access_request(req.webhook_url, req.requester, req.resource, req.justification)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-bulk-access-requests")
async def send_bulk_access_requests_api(req: BulkAccessRequest):
    result = await send_bulk_access_requests(req.webhook_url, req.requests)
    return result

@router.post("/teams/send-access-request-reminder")
async def send_access_request_reminder_api(req: AccessReminderRequest):
    result = await send_access_request_reminder(req.webhook_url, req.requester, req.resource)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result