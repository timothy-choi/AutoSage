from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxQuotaMonitorHelper import fetch_dropbox_quota

router = APIRouter()

class DropboxQuotaRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    human_readable: bool = Field(False, description="Return sizes in human-readable format")

@router.post("/dropbox/quota")
def dropbox_quota_monitor(request: DropboxQuotaRequest):
    try:
        result = fetch_dropbox_quota(
            access_token=request.access_token,
            human_readable=request.human_readable
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))