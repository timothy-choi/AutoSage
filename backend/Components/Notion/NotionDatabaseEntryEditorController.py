from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from NotionDatabaseEntryEditorHelper import edit_database_entry

router = APIRouter()

class NotionEntryEditRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    page_id: str = Field(..., description="ID of the Notion page to update")
    updated_properties: Dict[str, Any] = Field(..., description="New property values to set")

@router.patch("/notion/edit-database-entry")
def edit_notion_database_entry(request: NotionEntryEditRequest):
    try:
        result = edit_database_entry(
            notion_token=request.notion_token,
            page_id=request.page_id,
            updated_properties=request.updated_properties
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))