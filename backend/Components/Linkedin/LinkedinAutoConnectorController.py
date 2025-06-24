from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from LinkedinAutoConnectorHelper import send_bulk_connection_requests

router = APIRouter()

class LinkedInAutoConnectorRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 access token with invitation permissions")
    recipient_urns: List[str] = Field(..., description="List of LinkedIn URNs (e.g., 'urn:li:person:abc123')")
    message: Optional[str] = Field(None, description="Optional message to send with the connection request")

@router.post("/linkedin/auto-connect")
def auto_connect(request: LinkedInAutoConnectorRequest):
    if not request.recipient_urns:
        raise HTTPException(status_code=400, detail="You must provide at least one LinkedIn URN.")

    results = send_bulk_connection_requests(
        access_token=request.access_token,
        recipient_urns=request.recipient_urns,
        message=request.message
    )

    return {"results": results}