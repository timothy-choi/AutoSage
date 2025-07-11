from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxAutoOrganizerHelper import auto_organize_dropbox_files

router = APIRouter()

class DropboxAutoOrganizeRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    folder_path: str = Field("/", description="Path to folder to organize (default is root)")

@router.post("/dropbox/organize")
def dropbox_auto_organize(request: DropboxAutoOrganizeRequest):
    try:
        return auto_organize_dropbox_files(
            access_token=request.access_token,
            folder_path=request.folder_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))