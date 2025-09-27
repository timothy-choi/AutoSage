from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from YoutubeLiveStreamHelper import create_live_stream, list_scheduled_streams, end_live_broadcast
from typing import Optional

router = APIRouter(prefix="/youtube/live", tags=["YouTube Live Stream Helper"])


class CreateLiveStreamRequest(BaseModel):
    title: str
    description: str
    privacy_status: Optional[str] = "public"


@router.post("/create")
def api_create_live_stream(request: CreateLiveStreamRequest, authorization: str = Header(...)):
    try:
        return create_live_stream(
            access_token=authorization.replace("Bearer ", ""),
            title=request.title,
            description=request.description,
            privacy_status=request.privacy_status
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scheduled")
def api_list_scheduled_streams(
    max_results: int = Query(10, description="Max number of scheduled streams to return"),
    authorization: str = Header(...)
):
    try:
        return list_scheduled_streams(
            access_token=authorization.replace("Bearer ", ""),
            max_results=max_results
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/end/{broadcast_id}")
def api_end_live_broadcast(broadcast_id: str, authorization: str = Header(...)):
    try:
        return end_live_broadcast(
            access_token=authorization.replace("Bearer ", ""),
            broadcast_id=broadcast_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))