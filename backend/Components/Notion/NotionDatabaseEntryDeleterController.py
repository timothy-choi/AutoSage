from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionDatabaseEntryDeleterHelper import delete_database_entry

router = APIRouter()

class NotionEntryDeleteRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    page_id: str = Field(..., description="The ID of the Notion page (entry) to archive")

@router.delete("/notion/delete-database-entry")
def delete_notion_database_entry(request: NotionEntryDeleteRequest):
    try:
        result = delete_database_entry(
            notion_token=request.notion_token,
            page_id=request.page_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))