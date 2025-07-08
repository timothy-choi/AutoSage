from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from DropBoxFileUploaderHelper import upload_file_to_dropbox

router = APIRouter()

class DropboxUploadRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    local_file_path: str = Field(..., description="Path to the local file on disk")
    dropbox_dest_path: str = Field(..., description="Destination path in Dropbox (e.g., /myfolder/file.txt)")
    mode: Literal["add", "overwrite", "update"] = Field("add", description="Upload mode")

@router.post("/dropbox/upload")
def dropbox_upload(request: DropboxUploadRequest):
    try:
        result = upload_file_to_dropbox(
            access_token=request.access_token,
            local_file_path=request.local_file_path,
            dropbox_dest_path=request.dropbox_dest_path,
            mode=request.mode
        )
        return {"status": "success", "metadata": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))