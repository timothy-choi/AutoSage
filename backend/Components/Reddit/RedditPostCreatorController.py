from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditPostCreatorHelper import create_reddit_post

router = APIRouter()

class RedditPostRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditPostCreator/0.1 by YourBot")
    subreddit: str
    title: str
    body: str | None = None
    url: str | None = None

@router.post("/reddit/post")
def create_post(request: RedditPostRequest):
    try:
        if not request.body and not request.url:
            raise HTTPException(status_code=400, detail="Either 'body' or 'url' must be provided.")

        post_data = create_reddit_post(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            subreddit=request.subreddit,
            title=request.title,
            body=request.body,
            url=request.url
        )
        return {"status": "success", "post": post_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))