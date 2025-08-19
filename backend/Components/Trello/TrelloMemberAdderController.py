from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from TrelloMemberAdderHelper import add_member_to_board

router = APIRouter()

class TrelloMemberAddRequest(BaseModel):
    board_id: str = Field(..., description="ID of the Trello board")
    email: EmailStr = Field(..., description="Email of the member to invite")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")
    role: str = Field("normal", description="Role to assign (normal/admin)")

@router.post("/trello/member/add", tags=["Trello"])
async def trello_member_add(request: TrelloMemberAddRequest):
    try:
        result = add_member_to_board(
            board_id=request.board_id,
            email=request.email,
            api_key=request.api_key,
            token=request.token,
            role=request.role
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))