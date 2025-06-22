from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from TwitterTweetEditorHelper import simulate_edit_tweet

router = APIRouter()

class EditTweetPayload(BaseModel):
    tweet_id: str
    new_text: str
    media_id: Optional[str] = None

@router.post("/twitter/tweet/edit")
def edit_tweet(payload: EditTweetPayload):
    try:
        result = simulate_edit_tweet(payload.tweet_id, payload.new_text, payload.media_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))