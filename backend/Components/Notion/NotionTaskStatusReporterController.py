from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionTaskStatusReporterHelper import generate_status_report

router = APIRouter()

class TaskStatusReportRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="ID of the Notion task database")
    status_property: str = Field("Status", description="Name of the status property")
    max_pages: int = Field(100, description="Max number of pages to scan")

@router.post("/notion/task-status-report")
def task_status_report(request: TaskStatusReportRequest) -> Dict:
    try:
        return generate_status_report(
            notion_token=request.notion_token,
            database_id=request.database_id,
            status_property=request.status_property,
            max_pages=request.max_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))