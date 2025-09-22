from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PinterestBoardEditorHelper import edit_board, delete_board

router = APIRouter()

class BoardEditRequest(BaseModel):
    access_token: str
    board_id: str
    name: str | None = None
    description: str | None = None
    privacy: str | None = None  

class BoardDeleteRequest(BaseModel):
    access_token: str
    board_id: str


@router.patch("/pinterest/board/edit")
async def api_edit_board(request: BoardEditRequest):
    try:
        result = edit_board(
            access_token=request.access_token,
            board_id=request.board_id,
            name=request.name,
            description=request.description,
            privacy=request.privacy,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/pinterest/board/delete")
async def api_delete_board(request: BoardDeleteRequest):
    try:
        result = delete_board(
            access_token=request.access_token,
            board_id=request.board_id,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))