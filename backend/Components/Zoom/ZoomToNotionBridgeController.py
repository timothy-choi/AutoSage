from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from ZoomToNotionBridgeHelper import sync_zoom_meetings_to_notion

router = APIRouter()

class ZoomToNotionRequest(BaseModel):
    user_id: str = Field(..., description="Zoom user ID (e.g., 'me')")
    zoom_token: str = Field(..., description="Zoom JWT or OAuth token")
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Target Notion database ID")
    meeting_type: Literal["upcoming", "past"] = "upcoming"

@router.post("/zoom/sync-to-notion")
def zoom_to_notion_bridge(request: ZoomToNotionRequest):
    try:
        result = sync_zoom_meetings_to_notion(
            user_id=request.user_id,
            zoom_token=request.zoom_token,
            notion_token=request.notion_token,
            database_id=request.database_id,
            meeting_type=request.meeting_type
        )
        return {"synced": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))