from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TrelloLabelDeleterHelper import delete_label

router = APIRouter()

class TrelloLabelDeleteRequest(BaseModel):
    label_id: str = Field(..., description="Trello label ID to delete")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")

@router.delete("/trello/label/delete", tags=["Trello"])
async def trello_label_delete(request: TrelloLabelDeleteRequest):
    try:
        result = delete_label(
            label_id=request.label_id,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))