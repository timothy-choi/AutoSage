from fastapi import APIRouter, Header, HTTPException
from PinterestPinDeleterHelper import delete_pin

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Pins Deleter"])

@router.delete("/{pin_id}")
def api_delete_pin(pin_id: str, authorization: str = Header(...)):
    try:
        return delete_pin(authorization.replace("Bearer ", ""), pin_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))