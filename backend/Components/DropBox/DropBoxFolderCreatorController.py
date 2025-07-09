from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxFileUploaderController import create_dropbox_folder

router = APIRouter()

class DropboxFolderCreateRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    folder_path: str = Field(..., description="Dropbox folder path (e.g., /Projects/2025)")
    autorename: Optional[bool] = Field(False, description="Whether to rename if folder exists")

@router.post("/dropbox/create-folder")
def dropbox_create_folder(request: DropboxFolderCreateRequest):
    try:
        return create_dropbox_folder(
            access_token=request.access_token,
            folder_path=request.folder_path,
            autorename=request.autorename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))