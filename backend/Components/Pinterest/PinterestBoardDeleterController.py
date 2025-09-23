from fastapi import APIRouter, Header, HTTPException
from PinterestBoardDeleterHelper import delete_board

router = APIRouter(prefix="/pinterest/boards", tags=["Pinterest Board Deleter"])

@router.delete("/{board_id}")
def api_delete_board(board_id: str, authorization: str = Header(...)):
    try:
        return delete_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))