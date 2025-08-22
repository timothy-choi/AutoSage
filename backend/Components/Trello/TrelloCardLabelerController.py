from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TrelloCardLabelerHelper import add_label_to_card

router = APIRouter()

class TrelloLabelRequest(BaseModel):
    api_key: str
    token: str
    card_id: str
    label_id: str

@router.post("/trello/card/add-label")
def label_trello_card(request: TrelloLabelRequest):
    try:
        result = add_label_to_card(
            request.api_key,
            request.token,
            request.card_id,
            request.label_id
        )
        return {"status": "success", "label": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))