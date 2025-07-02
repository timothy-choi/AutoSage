from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleDrivePermissionSetterHelper import set_drive_permission

router = APIRouter()

class PermissionRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    file_id: str = Field(..., description="ID of the file or folder to share")
    role: str = Field(..., description="Access level: reader, commenter, writer")
    permission_type: str = Field(..., description="Type: user, group, domain, or anyone")
    email_address: Optional[str] = Field(None, description="Email for user/group permission")

@router.post("/gdrive/set-permission")
def set_permission(request: PermissionRequest):
    try:
        return set_drive_permission(
            access_token=request.access_token,
            file_id=request.file_id,
            role=request.role,
            permission_type=request.permission_type,
            email_address=request.email_address
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))