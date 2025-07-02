from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveLargeFileDetectorHelper import detect_large_files

router = APIRouter()

class LargeFileRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    size_threshold_mb: int = Field(100, description="Minimum file size in MB")
    max_results: int = Field(20, description="Maximum number of results to return")

@router.post("/gdrive/large-files")
def find_large_files(request: LargeFileRequest):
    try:
        return detect_large_files(
            access_token=request.access_token,
            size_threshold_mb=request.size_threshold_mb,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))