from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TrelloMemberRemoverHelper import remove_member_from_board

router = APIRouter()

class TrelloMemberRemoveRequest(BaseModel):
    board_id: str = Field(..., description="ID of the Trello board")
    member_id: str = Field(..., description="ID of the member to remove")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")

@router.delete("/trello/member/remove", tags=["Trello"])
async def trello_member_remove(request: TrelloMemberRemoveRequest):
    try:
        result = remove_member_from_board(
            board_id=request.board_id,
            member_id=request.member_id,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))