from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxSmartDuplicateDetectorHelper import smart_detect_dropbox_duplicates

router = APIRouter()

class DropboxDuplicateDetectRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    folder_path: str = Field("/", description="Folder to scan for duplicates")
    match_on: str = Field("content_hash", description="Match on 'content_hash' or 'name'")

@router.post("/dropbox/duplicates/detect")
def dropbox_detect_duplicates(request: DropboxDuplicateDetectRequest):
    try:
        return smart_detect_dropbox_duplicates(
            access_token=request.access_token,
            folder_path=request.folder_path,
            match_on=request.match_on
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))