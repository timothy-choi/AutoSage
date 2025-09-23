from fastapi import APIRouter, Header, HTTPException
from PinterestBoardFollowerManagerHelper import follow_board, unfollow_board, list_board_followers

router = APIRouter(prefix="/pinterest/boards/followers", tags=["Pinterest Board Followers"])

@router.post("/{board_id}/follow")
def api_follow_board(board_id: str, authorization: str = Header(...)):
    try:
        return follow_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{board_id}/unfollow")
def api_unfollow_board(board_id: str, authorization: str = Header(...)):
    try:
        return unfollow_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{board_id}")
def api_list_board_followers(board_id: str, authorization: str = Header(...)):
    try:
        return list_board_followers(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))