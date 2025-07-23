from fastapi import APIRouter, Query
from typing import List
from ConfluencePageDeleterHelper import (
    delete_confluence_page,
    delete_multiple_confluence_pages
)

router = APIRouter()

@router.delete("/confluence/page/delete")
def delete_single_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str = Query(..., description="ID of the Confluence page to delete")
):
    success = delete_confluence_page(base_url, username, api_token, page_id)
    if success:
        return {"status": "deleted", "page_id": page_id}
    return {"status": "failed", "page_id": page_id}


@router.delete("/confluence/pages/delete-bulk")
def delete_multiple_confluence_pages_endpoint(
    base_url: str,
    username: str,
    api_token: str,
    page_ids: List[str] = Query(..., description="List of Confluence page IDs to delete")
):
    results = delete_multiple_confluence_pages(base_url, username, api_token, page_ids)
    return {"results": results}