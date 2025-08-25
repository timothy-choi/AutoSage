from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditUpvoteHelper import upvote_item

router = APIRouter()

class RedditUpvoteRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditUpvoter/0.1 by YourBot")
    item_id: str 

@router.post("/reddit/upvote")
def reddit_upvote(request: RedditUpvoteRequest):
    try:
        result = upvote_item(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            item_id=request.item_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))