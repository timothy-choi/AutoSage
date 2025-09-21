from fastapi import APIRouter, Header, HTTPException
from PinterestPinCreatorHelper import update_pin

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Pins Editor"])

@router.patch("/{pin_id}")
def api_update_pin(
    pin_id: str,
    title: str = None,
    description: str = None,
    link: str = None,
    board_id: str = None,
    authorization: str = Header(...)
):
    try:
        return update_pin(
            authorization.replace("Bearer ", ""),
            pin_id,
            title,
            description,
            link,
            board_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))