from fastapi import APIRouter, Header, HTTPException, Query
from PinterestUserFollowerManagerHelper import (
    follow_user,
    unfollow_user,
    list_user_followers,
    list_user_following,
)

router = APIRouter(prefix="/pinterest/users/followers", tags=["Pinterest User Follower Manager"])


@router.post("/{user_id}/follow")
def api_follow_user(user_id: str, authorization: str = Header(...)):
    try:
        return follow_user(authorization.replace("Bearer ", ""), user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}/unfollow")
def api_unfollow_user(user_id: str, authorization: str = Header(...)):
    try:
        return unfollow_user(authorization.replace("Bearer ", ""), user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}")
def api_list_user_followers(
    user_id: str,
    limit: int = Query(25, description="Max number of followers to return"),
    authorization: str = Header(...)
):
    try:
        return list_user_followers(
            authorization.replace("Bearer ", ""),
            user_id,
            limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}/following")
def api_list_user_following(
    user_id: str,
    limit: int = Query(25, description="Max number of following users to return"),
    authorization: str = Header(...)
):
    try:
        return list_user_following(
            authorization.replace("Bearer ", ""),
            user_id,
            limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))