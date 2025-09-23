from fastapi import APIRouter, Header, HTTPException, Query
from PinterestBoardSearcherHelper import search_boards

router = APIRouter(prefix="/pinterest/boards/search", tags=["Pinterest Board Searcher"])

@router.get("/")
def api_search_boards(
    query: str = Query(..., description="Search query for boards"),
    limit: int = Query(25, description="Maximum number of results"),
    authorization: str = Header(...)
):
    try:
        return search_boards(
            access_token=authorization.replace("Bearer ", ""),
            query=query,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))