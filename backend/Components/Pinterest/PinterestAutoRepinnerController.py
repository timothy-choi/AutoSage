from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from PinterestAutoRepinnerHelper import repin_pin, bulk_repin

router = APIRouter(prefix="/pinterest/auto-repinner", tags=["Pinterest Auto Repinner"])

class RepinRequest(BaseModel):
    pin_id: str
    board_id: str
    note: Optional[str] = None

class BulkRepinRequest(BaseModel):
    pin_id: str
    board_ids: List[str]
    note: Optional[str] = None


@router.post("/repin")
def api_repin_pin(request: RepinRequest, authorization: str = Header(...)):
    try:
        return repin_pin(
            authorization.replace("Bearer ", ""),
            request.pin_id,
            request.board_id,
            request.note
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk-repin")
def api_bulk_repin(request: BulkRepinRequest, authorization: str = Header(...)):
    try:
        return bulk_repin(
            authorization.replace("Bearer ", ""),
            request.pin_id,
            request.board_ids,
            request.note
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))