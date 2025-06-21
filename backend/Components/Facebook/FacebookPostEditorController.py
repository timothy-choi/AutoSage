from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from FacebookPostEditorHelper import (
    edit_facebook_post,
    delete_facebook_post,
    get_facebook_post,
    list_facebook_posts,
    restore_facebook_post,
    bulk_edit_posts
)

router = APIRouter()

class EditPayload(BaseModel):
    post_id: str
    new_message: str

class DeletePayload(BaseModel):
    post_id: str

class RestorePayload(BaseModel):
    message: str

class BulkEditItem(BaseModel):
    post_id: str
    new_message: str

@router.put("/facebook/post/edit")
def edit_post(payload: EditPayload):
    try:
        return {"status": edit_facebook_post(payload.post_id, payload.new_message)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/facebook/post/delete/{post_id}")
def delete_post(post_id: str):
    try:
        return {"status": delete_facebook_post(post_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/facebook/post/get/{post_id}")
def get_post(post_id: str):
    try:
        return get_facebook_post(post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/facebook/post/list")
def list_posts(limit: int = 10):
    try:
        return {"posts": list_facebook_posts(limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/post/restore")
def restore_post(payload: RestorePayload):
    try:
        post_id = restore_facebook_post(payload.dict())
        return {"status": "restored", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/facebook/post/bulk-edit")
def bulk_edit(payload: List[BulkEditItem]):
    try:
        edits = [item.dict() for item in payload]
        results = bulk_edit_posts(edits)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))