from fastapi import APIRouter, Header, HTTPException
from BoxCommentManagerHelper import (
    create_comment,
    get_comment,
    list_comments,
    update_comment,
    delete_comment,
)

router = APIRouter(prefix="/box/comments", tags=["Box Comments"])

@router.post("/")
def api_create_comment(file_id: str, message: str, authorization: str = Header(...)):
    try:
        return create_comment(authorization.replace("Bearer ", ""), file_id, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{comment_id}")
def api_get_comment(comment_id: str, authorization: str = Header(...)):
    try:
        return get_comment(authorization.replace("Bearer ", ""), comment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file/{file_id}")
def api_list_comments(file_id: str, authorization: str = Header(...)):
    try:
        return list_comments(authorization.replace("Bearer ", ""), file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{comment_id}")
def api_update_comment(comment_id: str, message: str, authorization: str = Header(...)):
    try:
        return update_comment(authorization.replace("Bearer ", ""), comment_id, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{comment_id}")
def api_delete_comment(comment_id: str, authorization: str = Header(...)):
    try:
        return delete_comment(authorization.replace("Bearer ", ""), comment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))