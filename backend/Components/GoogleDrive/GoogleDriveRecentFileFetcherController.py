from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from GoogleDriveRecentFileFetcherHelper import fetch_recent_files

router = APIRouter()

class RecentFileRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 token with Drive access")
    max_results: int = Field(10, description="Number of files to fetch")
    sort_by: str = Field("modifiedTime", description="Field to sort by: modifiedTime or createdTime")

@router.post("/gdrive/recent-files")
def recent_files(request: RecentFileRequest) -> List[dict]:
    try:
        return fetch_recent_files(
            access_token=request.access_token,
            max_results=request.max_results,
            sort_by=request.sort_by
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))