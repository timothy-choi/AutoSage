from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Union
from GoogleDriveAccessRevokerHelper import revoke_drive_permission, list_drive_permissions

router = APIRouter()

class AccessRevokeRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    file_id: str = Field(..., description="ID of the file or folder")
    permission_id: Optional[str] = Field(None, description="Permission ID to revoke (optional)")

@router.post("/gdrive/revoke-access")
def revoke_access(request: AccessRevokeRequest):
    try:
        if request.permission_id:
            return revoke_drive_permission(
                access_token=request.access_token,
                file_id=request.file_id,
                permission_id=request.permission_id
            )
        else:
            permissions = list_drive_permissions(
                access_token=request.access_token,
                file_id=request.file_id
            )
            return {
                "status": "permission_list",
                "file_id": request.file_id,
                "permissions": permissions
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))