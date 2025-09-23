from fastapi import APIRouter, Header, HTTPException, Query
from PinterestPinSearcherHelper import search_pins

router = APIRouter(prefix="/pinterest/pins/search", tags=["Pinterest Pin Searcher"])

@router.get("/")
def api_search_pins(
    query: str = Query(..., description="Search query for pins"),
    board_id: str | None = Query(None, description="Optional board ID to filter search"),
    limit: int = Query(25, description="Maximum number of results"),
    authorization: str = Header(...)
):
    try:
        return search_pins(
            access_token=authorization.replace("Bearer ", ""),
            query=query,
            board_id=board_id,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))