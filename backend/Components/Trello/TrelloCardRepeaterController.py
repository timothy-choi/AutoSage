from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TrelloCardRepeaterHelper import repeat_trello_card

router = APIRouter()

class TrelloCardRepeatRequest(BaseModel):
    card_id: str = Field(..., description="The ID of the Trello card to copy")
    target_list_id: str = Field(..., description="The ID of the Trello list to copy the card to")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")

@router.post("/trello/card/repeat", tags=["Trello"])
async def repeat_card(request: TrelloCardRepeatRequest):
    try:
        result = repeat_trello_card(
            card_id=request.card_id,
            target_list_id=request.target_list_id,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))