from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionRecurringTaskSchedulerHelper import create_recurring_task

router = APIRouter()

class RecurringTaskRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="Target Notion database ID")
    template: Dict = Field(..., description="Task template to duplicate")
    frequency: str = Field(..., description="Recurrence frequency: daily, weekly, monthly")

@router.post("/notion/recurring-task")
def schedule_recurring_task(request: RecurringTaskRequest) -> Dict:
    try:
        return create_recurring_task(
            notion_token=request.notion_token,
            database_id=request.database_id,
            template=request.template,
            frequency=request.frequency
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))