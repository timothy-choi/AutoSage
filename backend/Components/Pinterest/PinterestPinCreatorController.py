from fastapi import APIRouter, Header, HTTPException
from PinterestPinCreatorHelper import (
    create_pin,
    get_pin,
    delete_pin,
    list_pins_on_board,
)

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Pins"])

@router.post("/")
def api_create_pin(
    board_id: str,
    title: str,
    description: str,
    media_url: str,
    link: str = None,
    authorization: str = Header(...)
):
    try:
        return create_pin(authorization.replace("Bearer ", ""), board_id, title, description, media_url, link)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pin_id}")
def api_get_pin(pin_id: str, authorization: str = Header(...)):
    try:
        return get_pin(authorization.replace("Bearer ", ""), pin_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pin_id}")
def api_delete_pin(pin_id: str, authorization: str = Header(...)):
    try:
        return delete_pin(authorization.replace("Bearer ", ""), pin_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/board/{board_id}")
def api_list_pins(board_id: str, authorization: str = Header(...)):
    try:
        return list_pins_on_board(authorization.replace("Bearer ", ""), board_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))