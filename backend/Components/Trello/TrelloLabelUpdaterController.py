from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from TrelloLabelUpdaterHelper import update_label

router = APIRouter()

class LabelUpdateRequest(BaseModel):
    label_id: str = Field(..., description="ID of the Trello label")
    name: Optional[str] = Field(None, description="New name for the label")
    color: Optional[str] = Field(None, description="New color for the label")
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")

@router.put("/trello/label/update", tags=["Trello"])
async def trello_label_update(request: LabelUpdateRequest):
    try:
        result = update_label(
            label_id=request.label_id,
            name=request.name,
            color=request.color,
            api_key=request.api_key,
            token=request.token
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))