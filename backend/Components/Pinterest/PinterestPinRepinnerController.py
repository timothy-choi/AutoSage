from fastapi import APIRouter, Header, HTTPException
from PinterestPinRepinnerHelper import repin

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Pins Repinner"])

@router.post("/repin")
def api_repin(
    board_id: str,
    parent_pin_id: str,
    title: str = None,
    description: str = None,
    authorization: str = Header(...)
):
    try:
        return repin(
            authorization.replace("Bearer ", ""),
            board_id,
            parent_pin_id,
            title,
            description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))