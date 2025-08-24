from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditCommentEditorHelper import edit_reddit_comment

router = APIRouter()

class RedditCommentEditRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditCommentEditor/0.1 by YourBot")
    comment_id: str
    new_text: str

@router.put("/reddit/comment")
def edit_comment(request: RedditCommentEditRequest):
    try:
        result = edit_reddit_comment(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            comment_id=request.comment_id,
            new_text=request.new_text
        )
        return {"status": "success", "result": result}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))