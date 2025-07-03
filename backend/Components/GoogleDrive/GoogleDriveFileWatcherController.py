from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleDriveFileWatcherHelper import get_start_page_token, fetch_drive_changes

router = APIRouter()

class ChangeWatcherRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    start_page_token: Optional[str] = Field(None, description="Last known startPageToken")
    max_results: int = Field(100, description="Max changes to fetch")

@router.post("/gdrive/watch-changes")
def watch_changes(request: ChangeWatcherRequest):
    try:
        token = request.start_page_token or get_start_page_token(request.access_token)
        result = fetch_drive_changes(
            access_token=request.access_token,
            start_page_token=token,
            max_results=request.max_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))