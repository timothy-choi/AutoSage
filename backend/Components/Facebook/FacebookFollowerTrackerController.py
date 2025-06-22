from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from FacebookFollowerTrackerHelper import (
    fetch_follower_count,
    fetch_daily_followers,
    fetch_page_info_with_followers
)

router = APIRouter()

class ComparePagesPayload(BaseModel):
    page_ids: List[str]

@router.get("/facebook/followers/{page_id}")
def get_current_follower_count(page_id: str):
    try:
        data = fetch_follower_count(page_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/facebook/followers/{page_id}/info")
def get_page_info_with_followers(page_id: str):
    try:
        return fetch_page_info_with_followers(page_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/facebook/followers/{page_id}/daily")
def get_daily_followers(page_id: str, days: int = Query(7, ge=1, le=30)):
    try:
        return fetch_daily_followers(page_id, days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))