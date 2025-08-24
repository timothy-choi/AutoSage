from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditCommentDeleterHelper import delete_reddit_comment

router = APIRouter()

class RedditCommentDeleteRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditCommentDeleter/0.1 by YourBot")
    comment_id: str  

@router.delete("/reddit/comment")
def delete_comment(request: RedditCommentDeleteRequest):
    try:
        result = delete_reddit_comment(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            comment_id=request.comment_id
        )
        return {"status": "success", "result": result}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))