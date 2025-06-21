from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from FacebookCommentModeratorHelper import (
    list_comments,
    hide_comment,
    delete_comment,
    reply_to_comment
)

router = APIRouter()

class CommentActionPayload(BaseModel):
    comment_id: str

class CommentReplyPayload(BaseModel):
    comment_id: str
    message: str

@router.get("/facebook/comments/{post_id}")
def fetch_comments(post_id: str, limit: int = 10):
    try:
        comments = list_comments(post_id, limit)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/comments/hide")
def hide(payload: CommentActionPayload):
    try:
        return {"status": hide_comment(payload.comment_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/comments/delete")
def delete(payload: CommentActionPayload):
    try:
        return {"status": delete_comment(payload.comment_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/comments/reply")
def reply(payload: CommentReplyPayload):
    try:
        comment_id = reply_to_comment(payload.comment_id, payload.message)
        return {"status": "replied", "reply_id": comment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))