from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from DropBoxFileSearcherHelper import search_files_in_dropbox

router = APIRouter()

class DropboxSearchRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    query: str = Field(..., description="Search keyword (e.g., 'report')")
    path: Optional[str] = Field("", description="Path to search within (e.g., '/docs')")
    max_results: Optional[int] = Field(10, description="Maximum number of results to return")
    file_extensions: Optional[List[str]] = Field(None, description="Filter results by file extensions (e.g., ['pdf'])")

@router.post("/dropbox/search")
def dropbox_search(request: DropboxSearchRequest):
    try:
        return search_files_in_dropbox(
            access_token=request.access_token,
            query=request.query,
            path=request.path,
            max_results=request.max_results,
            file_extensions=request.file_extensions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))