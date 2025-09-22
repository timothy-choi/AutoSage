from fastapi import APIRouter, Header, HTTPException
from PinterestBoardCreatorHelper import (
    create_board,
    get_board,
    delete_board,
    list_boards,
)

router = APIRouter(prefix="/pinterest/boards", tags=["Pinterest Boards"])

@router.post("/")
def api_create_board(
    name: str,
    description: str = None,
    privacy: str = "PUBLIC",
    authorization: str = Header(...)
):
    try:
        return create_board(
            authorization.replace("Bearer ", ""),
            name,
            description,
            privacy
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{board_id}")
def api_get_board(board_id: str, authorization: str = Header(...)):
    try:
        return get_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{board_id}")
def api_delete_board(board_id: str, authorization: str = Header(...)):
    try:
        return delete_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def api_list_boards(authorization: str = Header(...)):
    try:
        return list_boards(authorization.replace("Bearer ", ""))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))