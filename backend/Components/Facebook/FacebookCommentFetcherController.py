from fastapi import APIRouter, HTTPException
from FacebookCommentFetcherHelper import (
    fetch_comments,
    fetch_comment_replies
)

router = APIRouter()

@router.get("/facebook/comments/fetch/{post_id}")
def get_comments(post_id: str, limit: int = 10):
    try:
        return {"comments": fetch_comments(post_id, limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/facebook/comments/replies/{comment_id}")
def get_replies(comment_id: str, limit: int = 10):
    try:
        return {"replies": fetch_comment_replies(comment_id, limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))