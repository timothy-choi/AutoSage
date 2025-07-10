from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxPermissionFileSetterHelper import set_dropbox_file_permissions

router = APIRouter()

class DropboxPermissionRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path to the shared file or folder")
    requested_visibility: Optional[str] = Field("public", description="One of: public, team_only, password")
    allow_download: Optional[bool] = Field(True, description="Allow downloads or not")
    password: Optional[str] = Field(None, description="Password if using 'password' visibility")
    expires: Optional[str] = Field(None, description="Expiration timestamp (ISO8601)")

@router.post("/dropbox/permissions/set")
def dropbox_set_permissions(request: DropboxPermissionRequest):
    try:
        return set_dropbox_file_permissions(
            access_token=request.access_token,
            path=request.path,
            requested_visibility=request.requested_visibility,
            allow_download=request.allow_download,
            password=request.password,
            expires=request.expires
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))