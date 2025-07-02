from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from GoogleDriveFileSearcherHelper import search_drive_files

router = APIRouter()

class FileSearchRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 token")
    name_query: Optional[str] = Field(None, description="Partial name match (e.g., 'report')")
    mime_type: Optional[str] = Field(None, description="MIME type filter (e.g., 'application/pdf')")
    custom_q: Optional[str] = Field(None, description="Custom Google Drive query string")
    max_results: int = Field(10, description="Number of results to return (default: 10)")

@router.post("/gdrive/search-files")
def search_files(request: FileSearchRequest) -> List[dict]:
    try:
        return search_drive_files(
            access_token=request.access_token,
            name_query=request.name_query,
            mime_type=request.mime_type,
            custom_q=request.custom_q,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))