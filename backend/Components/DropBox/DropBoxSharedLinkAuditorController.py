from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxSharedLinkAuditorHelper import audit_dropbox_shared_links

router = APIRouter()

class DropboxAuditRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API token")
    path: Optional[str] = Field(None, description="Optional path to audit specific file/folder")

@router.post("/dropbox/shared-links/audit")
def dropbox_shared_link_audit(request: DropboxAuditRequest):
    try:
        return audit_dropbox_shared_links(
            access_token=request.access_token,
            path=request.path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))