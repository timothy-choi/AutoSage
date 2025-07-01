from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from ZoomUserPresenceCheckerHelper import get_multiple_user_presences

router = APIRouter()

class UserPresenceCheckRequest(BaseModel):
    jwt_token: str = Field(..., description="Zoom JWT or OAuth token")
    user_ids: List[str] = Field(..., description="List of Zoom user IDs or emails")

@router.post("/zoom/check-user-presence")
def check_zoom_user_presence(request: UserPresenceCheckRequest):
    try:
        results = get_multiple_user_presences(request.user_ids, request.jwt_token)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))