from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from PinterestAutoBoardOrganizerHelper import reorder_pins_in_board, move_pin_to_board, clean_old_pins

router = APIRouter(prefix="/pinterest/auto-board-organizer", tags=["Pinterest Auto Board Organizer"])

class ReorderRequest(BaseModel):
    board_id: str
    pin_ids: List[str]

class MoveRequest(BaseModel):
    pin_id: str
    new_board_id: str

class CleanRequest(BaseModel):
    board_id: str
    limit: Optional[int] = 50


@router.post("/reorder")
def api_reorder_pins(request: ReorderRequest, authorization: str = Header(...)):
    try:
        return reorder_pins_in_board(
            authorization.replace("Bearer ", ""),
            request.board_id,
            request.pin_ids
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/move")
def api_move_pin(request: MoveRequest, authorization: str = Header(...)):
    try:
        return move_pin_to_board(
            authorization.replace("Bearer ", ""),
            request.pin_id,
            request.new_board_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clean")
def api_clean_old_pins(request: CleanRequest, authorization: str = Header(...)):
    try:
        return clean_old_pins(
            authorization.replace("Bearer ", ""),
            request.board_id,
            request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))