from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxSharedLinkGeneratorHelper import generate_dropbox_shared_link

router = APIRouter()

class DropboxSharedLinkRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path of the file/folder to share (e.g., /docs/report.pdf)")
    visibility: Optional[str] = Field("public", description="Link visibility: public, team_only, password")
    allow_download: Optional[bool] = Field(True, description="Whether to allow downloads")
    password: Optional[str] = Field(None, description="Password for link (if using 'password' visibility)")
    expires: Optional[str] = Field(None, description="Expiration time (ISO8601, e.g. 2025-08-01T12:00:00Z)")

@router.post("/dropbox/share")
def dropbox_generate_link(request: DropboxSharedLinkRequest):
    try:
        return generate_dropbox_shared_link(
            access_token=request.access_token,
            path=request.path,
            visibility=request.visibility,
            allow_download=request.allow_download,
            password=request.password,
            expires=request.expires
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))