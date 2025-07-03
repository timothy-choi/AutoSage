from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleCalendarEventMoverHelper import move_calendar_event

router = APIRouter()

class EventMoveRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token with calendar scope")
    source_calendar_id: str = Field("primary", description="Source calendar ID")
    event_id: str = Field(..., description="ID of the event to move")
    target_calendar_id: str = Field(..., description="Target calendar ID")

@router.post("/gcalendar/move-event")
def move_event(request: EventMoveRequest):
    try:
        return move_calendar_event(
            access_token=request.access_token,
            source_calendar_id=request.source_calendar_id,
            event_id=request.event_id,
            target_calendar_id=request.target_calendar_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))