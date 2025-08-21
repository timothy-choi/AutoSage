from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TrelloAutoRemoverHelper import auto_move_cards

router = APIRouter()

class TrelloAutoMoverRequest(BaseModel):
    source_list_id: str = Field(..., description="Trello source list ID")
    target_list_id: str = Field(..., description="Trello target list ID")
    condition: str = Field(..., description="Condition to auto-move cards", example="past_due")
    api_key: str
    token: str

@router.post("/trello/card/auto-move", tags=["Trello"])
async def auto_move_trello_cards(request: TrelloAutoMoverRequest):
    try:
        moved = auto_move_cards(
            source_list_id=request.source_list_id,
            target_list_id=request.target_list_id,
            condition=request.condition,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "moved_cards": moved}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))