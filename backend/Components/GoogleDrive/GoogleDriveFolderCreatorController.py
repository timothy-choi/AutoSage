from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveFolderCreatorHelper import create_drive_folder

router = APIRouter()

class FolderCreateRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    folder_name: str = Field(..., description="Name of the folder to create")
    parent_folder_id: str = Field(None, description="Optional ID of the parent folder")

@router.post("/gdrive/create-folder")
def create_folder(request: FolderCreateRequest):
    try:
        return create_drive_folder(
            access_token=request.access_token,
            folder_name=request.folder_name,
            parent_folder_id=request.parent_folder_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))