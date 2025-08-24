from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditCommenterHelper import comment_on_reddit

router = APIRouter()

class RedditCommentRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditCommenter/0.1 by YourBot")
    target_id: str 
    text: str

@router.post("/reddit/comment")
def post_comment(request: RedditCommentRequest):
    try:
        result = comment_on_reddit(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            target_id=request.target_id,
            text=request.text,
        )
        return {"status": "success", "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))