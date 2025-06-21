from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from FacebookPostDeleterHelper import (
    delete_facebook_post,
    soft_delete_post,
    undo_deleted_post,
    delete_multiple_posts,
    delete_posts_by_keyword,
    delete_old_posts
)

router = APIRouter()

class PostIDPayload(BaseModel):
    post_id: str

class PostDataPayload(BaseModel):
    message: str

class BatchDeletePayload(BaseModel):
    post_ids: List[str]

class KeywordDeletePayload(BaseModel):
    keyword: str

class AgeDeletePayload(BaseModel):
    days_old: int

@router.delete("/facebook/post/delete")
def delete_post(payload: PostIDPayload):
    try:
        return {"status": delete_facebook_post(payload.post_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/post/soft-delete")
def soft_delete(payload: PostIDPayload):
    try:
        return {"status": soft_delete_post(payload.post_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/post/undo")
def restore(payload: PostDataPayload):
    try:
        post_id = undo_deleted_post(payload.dict())
        return {"status": "restored", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/post/delete-multiple")
def delete_batch(payload: BatchDeletePayload):
    try:
        return {"results": delete_multiple_posts(payload.post_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/post/delete-by-keyword")
def delete_by_keyword(payload: KeywordDeletePayload):
    try:
        deleted = delete_posts_by_keyword(payload.keyword)
        return {"deleted_posts": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/post/delete-old")
def delete_old(payload: AgeDeletePayload):
    try:
        deleted = delete_old_posts(payload.days_old)
        return {"deleted_posts": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))