from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional
from ConfluenceBulkPageCreatorHelper import create_bulk_confluence_pages

router = APIRouter()

class PageData(BaseModel):
    title: str
    body: str
    parent_id: Optional[str] = None

class BulkPageRequest(BaseModel):
    base_url: str
    username: str
    api_token: str
    space_key: str
    pages: List[PageData]

@router.post("/confluence/pages/bulk-create")
def bulk_create_confluence_pages(request: BulkPageRequest):
    return create_bulk_confluence_pages(
        base_url=request.base_url,
        username=request.username,
        api_token=request.api_token,
        space_key=request.space_key,
        pages=[page.dict() for page in request.pages]
    )