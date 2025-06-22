from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TwitterThreadBuilderHelper import post_tweet_thread

router = APIRouter()

class ThreadInput(BaseModel):
    tweets: List[str]

@router.post("/twitter/thread")
def create_twitter_thread(payload: ThreadInput):
    try:
        result = post_tweet_thread(payload.tweets)
        return {"status": "posted", "thread": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))