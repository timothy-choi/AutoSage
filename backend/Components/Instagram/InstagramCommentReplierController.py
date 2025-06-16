from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramCommentReplierHelper import reply_to_comment, like_comment, delete_comment

router = APIRouter()

class CommentReplyRequest(BaseModel):
    comment_id: str
    message: str
    access_token: str

class CommentActionRequest(BaseModel):
    comment_id: str
    access_token: str

@router.post("/instagram/reply-to-comment")
async def reply_to_comment_api(req: CommentReplyRequest):
    result = await reply_to_comment(req.comment_id, req.message, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/like-comment")
async def like_comment_api(req: CommentActionRequest):
    result = await like_comment(req.comment_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.delete("/instagram/delete-comment")
async def delete_comment_api(req: CommentActionRequest):
    result = await delete_comment(req.comment_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result