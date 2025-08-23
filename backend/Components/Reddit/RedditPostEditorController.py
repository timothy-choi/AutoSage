from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditPostEditorHelper import edit_reddit_post

router = APIRouter()

class RedditEditRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditPostEditor/0.1 by YourBot")
    post_id: str
    new_text: str

@router.put("/reddit/post")
def edit_post(request: RedditEditRequest):
    try:
        result = edit_reddit_post(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            post_id=request.post_id,
            new_text=request.new_text,
        )
        return {"status": "success", "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))