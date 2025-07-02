from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from NotionTaskPrioritizerHelper import prioritize_tasks

router = APIRouter()

class NotionPriorityRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="ID of the Notion database")
    max_tasks: int = Field(10, description="Number of tasks to prioritize")

@router.post("/notion/prioritize-tasks")
def prioritize_notion_tasks(request: NotionPriorityRequest) -> List[Dict]:
    try:
        return prioritize_tasks(
            notion_token=request.notion_token,
            database_id=request.database_id,
            max_tasks=request.max_tasks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))