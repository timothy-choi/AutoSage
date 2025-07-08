from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxFileDownloadHelper import download_file_from_dropbox

router = APIRouter()

class DropboxDownloadRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    dropbox_file_path: str = Field(..., description="Path of the file in Dropbox (e.g., /docs/file.pdf)")
    local_dest_path: str = Field(..., description="Path to save the file locally (e.g., ./downloads/file.pdf)")

@router.post("/dropbox/download")
def dropbox_download(request: DropboxDownloadRequest):
    try:
        result = download_file_from_dropbox(
            access_token=request.access_token,
            dropbox_file_path=request.dropbox_file_path,
            local_dest_path=request.local_dest_path
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))