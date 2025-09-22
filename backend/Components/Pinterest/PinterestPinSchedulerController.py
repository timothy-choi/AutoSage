from fastapi import APIRouter, Header, HTTPException
from PinterestPinSchedulerHelper import schedule_pin

router = APIRouter(prefix="/pinterest/pins", tags=["Pinterest Pins Scheduler"])

@router.post("/schedule")
def api_schedule_pin(
    board_id: str,
    title: str,
    description: str,
    media_url: str,
    scheduled_time: int,   
    link: str = None,
    authorization: str = Header(...)
):
    try:
        return schedule_pin(
            authorization.replace("Bearer ", ""),
            board_id,
            title,
            description,
            media_url,
            scheduled_time,
            link
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))