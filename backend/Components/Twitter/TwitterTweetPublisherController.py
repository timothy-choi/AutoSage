from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from TwitterTweetPublisherHelper import (
    post_tweet
)

router = APIRouter()

class TweetInput(BaseModel):
    text: str
    media_id: Optional[str] = None

class ScheduledTweetInput(BaseModel):
    text: str
    post_at: datetime

@router.post("/twitter/tweet")
def publish_tweet(payload: TweetInput):
    try:
        result = post_tweet(payload.text, payload.media_id)
        return {"status": "posted", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))