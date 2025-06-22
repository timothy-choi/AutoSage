from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from TwitterReplyHandlerHelper import reply_to_tweet

router = APIRouter()

class ReplyInput(BaseModel):
    text: str
    in_reply_to_tweet_id: str
    media_id: Optional[str] = None

@router.post("/twitter/reply")
def send_reply(payload: ReplyInput):
    try:
        result = reply_to_tweet(
            reply_text=payload.text,
            in_reply_to_tweet_id=payload.in_reply_to_tweet_id,
            media_id=payload.media_id
        )
        return {"status": "replied", "tweet": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))