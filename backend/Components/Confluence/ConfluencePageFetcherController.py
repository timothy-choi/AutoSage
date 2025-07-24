from fastapi import APIRouter, Query
from typing import List
from ConfluencePageFetcherHelper import (
    fetch_confluence_page,
    fetch_confluence_pages_by_space
)

router = APIRouter()

@router.get("/confluence/page/fetch")
def get_confluence_page(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str = Query(..., description="ID of the Confluence page")
):
    return fetch_confluence_page(base_url, username, api_token, page_id)

@router.get("/confluence/pages/fetch-by-space")
def get_pages_by_space(
    base_url: str,
    username: str,
    api_token: str,
    space_key: str = Query(..., description="Space key to fetch pages from"),
    limit: int = Query(25, description="Number of pages to retrieve")
):
    return fetch_confluence_pages_by_space(base_url, username, api_token, space_key, limit)