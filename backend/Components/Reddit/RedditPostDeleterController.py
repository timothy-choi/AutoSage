from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditPostDeleterHelper import delete_reddit_post

router = APIRouter()

class RedditDeleteRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditPostDeleter/0.1 by YourBot")
    post_id: str

@router.delete("/reddit/post")
def delete_post(request: RedditDeleteRequest):
    try:
        result = delete_reddit_post(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            post_id=request.post_id
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))