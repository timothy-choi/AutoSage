from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TrelloPermissionManagerHelper import update_member_permission

router = APIRouter()

class TrelloPermissionUpdateRequest(BaseModel):
    board_id: str = Field(..., description="ID of the Trello board")
    member_id: str = Field(..., description="ID of the member")
    permission_level: str = Field(..., description="Permission level (normal, admin, observer)")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")

@router.put("/trello/permissions/update", tags=["Trello"])
async def update_trello_permission(request: TrelloPermissionUpdateRequest):
    try:
        result = update_member_permission(
            board_id=request.board_id,
            member_id=request.member_id,
            permission_level=request.permission_level,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "data": result}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))