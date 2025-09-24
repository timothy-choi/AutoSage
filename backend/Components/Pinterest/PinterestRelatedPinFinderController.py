from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from PinterestRelatedPinFinderHelper import (
    find_related_pins,
    bulk_find_related_pins,
    get_recommended_pins,
)

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Related Pin Finder"])

class BulkRelatedRequest(BaseModel):
    pin_ids: list[str]
    limit: int = 10

@router.get("/related/{pin_id}")
def api_find_related_pins(
    pin_id: str,
    limit: int = Query(25, description="Max number of related pins"),
    media_type: str | None = Query(None, description="Optional filter: image or video"),
    authorization: str = Header(...)
):
    try:
        return find_related_pins(
            access_token=authorization.replace("Bearer ", ""),
            pin_id=pin_id,
            limit=limit,
            media_type=media_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/related/bulk")
def api_bulk_find_related_pins(
    request: BulkRelatedRequest,
    authorization: str = Header(...)
):
    try:
        return bulk_find_related_pins(
            access_token=authorization.replace("Bearer ", ""),
            pin_ids=request.pin_ids,
            limit=request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommended")
def api_get_recommended_pins(
    limit: int = Query(25, description="Max number of recommendations"),
    authorization: str = Header(...)
):
    try:
        return get_recommended_pins(
            access_token=authorization.replace("Bearer ", ""),
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))