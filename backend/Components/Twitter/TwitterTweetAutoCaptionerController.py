from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitterTweetAutoCaptionerHelper import generate_caption

router = APIRouter()

class CaptionInput(BaseModel):
    text: str

@router.post("/twitter/tweet/auto-caption")
def auto_caption_tweet(payload: CaptionInput):
    try:
        return generate_caption(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))