from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxNewUploadNotifierHelper import notify_new_uploads

router = APIRouter()

class DropboxUploadNotifierRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    folder_path: Optional[str] = Field("/", description="Folder to monitor for new uploads")
    cursor: Optional[str] = Field(None, description="Last known cursor (for polling)")

@router.post("/dropbox/uploads/notify")
def dropbox_new_upload_notify(request: DropboxUploadNotifierRequest):
    try:
        return notify_new_uploads(
            access_token=request.access_token,
            cursor=request.cursor,
            folder_path=request.folder_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))