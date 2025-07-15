from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxSharedFileFetcherHelper import fetch_dropbox_shared_files

router = APIRouter()

class DropboxSharedFileRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    path: Optional[str] = Field(None, description="Optional path to filter shared items")
    direct_only: Optional[bool] = Field(False, description="Only include directly shared files")

@router.post("/dropbox/shared-files")
def dropbox_shared_file_fetcher(request: DropboxSharedFileRequest):
    try:
        results = fetch_dropbox_shared_files(
            access_token=request.access_token,
            path=request.path,
            direct_only=request.direct_only
        )
        return {
            "shared_file_count": len(results),
            "shared_files": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))