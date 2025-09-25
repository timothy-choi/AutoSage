from fastapi import APIRouter, Header, HTTPException, Query
from PinterestPinLikeManagerHelper import like_pin, unlike_pin, list_pin_likes

router = APIRouter(prefix="/pinterest/pins/likes", tags=["Pinterest Pin Like Manager"])


@router.post("/{pin_id}/like")
def api_like_pin(pin_id: str, authorization: str = Header(...)):
    try:
        return like_pin(authorization.replace("Bearer ", ""), pin_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{pin_id}/unlike")
def api_unlike_pin(pin_id: str, authorization: str = Header(...)):
    try:
        return unlike_pin(authorization.replace("Bearer ", ""), pin_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pin_id}")
def api_list_pin_likes(
    pin_id: str,
    limit: int = Query(25, description="Max number of users to return"),
    authorization: str = Header(...)
):
    try:
        return list_pin_likes(authorization.replace("Bearer ", ""), pin_id, limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))