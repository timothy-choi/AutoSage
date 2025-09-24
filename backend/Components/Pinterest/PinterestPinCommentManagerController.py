from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from PinterestPinCommentManagerHelper import create_comment, list_comments, delete_comment

router = APIRouter(prefix="/pinterest/pins/comments", tags=["Pinterest Pin Comment Manager"])

class CommentCreateRequest(BaseModel):
    pin_id: str
    text: str


@router.post("/")
def api_create_comment(request: CommentCreateRequest, authorization: str = Header(...)):
    try:
        return create_comment(
            authorization.replace("Bearer ", ""),
            request.pin_id,
            request.text
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pin_id}")
def api_list_comments(
    pin_id: str,
    limit: int = Query(25, description="Max number of comments to fetch"),
    authorization: str = Header(...)
):
    try:
        return list_comments(
            authorization.replace("Bearer ", ""),
            pin_id,
            limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{pin_id}/{comment_id}")
def api_delete_comment(pin_id: str, comment_id: str, authorization: str = Header(...)):
    try:
        return delete_comment(
            authorization.replace("Bearer ", ""),
            pin_id,
            comment_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))