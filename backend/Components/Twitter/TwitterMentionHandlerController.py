from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from TwitterMentionHandlerHelper import fetch_recent_mentions, extract_mention_info

router = APIRouter()

@router.get("/twitter/mentions")
def get_recent_mentions(since_id: Optional[str] = Query(None), count: int = Query(10, ge=1, le=100)):
    try:
        raw_mentions = fetch_recent_mentions(since_id, count)
        simplified = [extract_mention_info(m) for m in raw_mentions]
        return simplified
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
