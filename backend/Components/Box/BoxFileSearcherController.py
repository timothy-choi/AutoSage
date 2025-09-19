from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from BoxFileSearcherHelper import search_files

router = APIRouter(prefix="/box/search", tags=["Box Search"])

class BoxFileSearchRequest(BaseModel):
    query: str
    ancestor_folder_id: Optional[str] = None
    file_extensions: Optional[List[str]] = None
    limit: int = 100

@router.get("/")
def search_box_files(
    query: str = Query(..., description="Search query"),
    ancestor_folder_id: Optional[str] = Query(None, description="Folder ID to limit search"),
    file_extensions: Optional[List[str]] = Query(None, description="Filter by file extensions"),
    limit: int = Query(100, description="Maximum results")
):
    return search_files(query, ancestor_folder_id, file_extensions, limit)