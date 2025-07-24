from fastapi import APIRouter, Query
from ConfluencePageRestorerHelper import restore_confluence_page

router = APIRouter()

@router.post("/confluence/page/restore")
def restore_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str = Query(..., description="ID of the Confluence page to restore")
):
    """
    Restore a Confluence page from the trash.
    """
    return restore_confluence_page(base_url, username, api_token, page_id)