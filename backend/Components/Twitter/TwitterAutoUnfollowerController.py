from fastapi import APIRouter, HTTPException, Query
from TwitterAutoUnfollowerHelper import auto_unfollow_nonfollowers

router = APIRouter()

@router.post("/twitter/unfollow-nonfollowers")
def unfollow_nonfollowers(screen_name: str = Query(...), limit: int = Query(10, ge=1, le=100)):
    try:
        return auto_unfollow_nonfollowers(screen_name, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))