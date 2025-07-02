from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionKanbanMoverHelper import move_kanban_card

router = APIRouter()

class KanbanMoveRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    page_id: str = Field(..., description="ID of the task or page to update")
    new_status: str = Field(..., description="New status column (e.g., 'In Progress')")
    status_property_name: str = Field("Status", description="Name of the status property (default: 'Status')")

@router.post("/notion/kanban-move")
def move_card(request: KanbanMoveRequest):
    try:
        return move_kanban_card(
            notion_token=request.notion_token,
            page_id=request.page_id,
            new_status=request.new_status,
            status_property_name=request.status_property_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))