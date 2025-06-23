from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from TwitterLikeRetweetMonitorHelper import (
    fetch_recent_likes,
    fetch_retweets,
    summarize_likes,
    summarize_retweets
)

router = APIRouter()

@router.get("/twitter/likes")
def get_recent_likes(screen_name: str = Query(...), count: int = Query(10, ge=1, le=100)):
    try:
        raw_likes = fetch_recent_likes(screen_name, count)
        return summarize_likes(raw_likes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/twitter/retweets")
def get_retweets(tweet_id: str = Query(...), count: int = Query(10, ge=1, le=100)):
    try:
        raw_retweets = fetch_retweets(tweet_id, count)
        return summarize_retweets(raw_retweets)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))