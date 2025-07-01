from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from NotionDatabaseEntryCreatorHelper import create_database_entry

router = APIRouter()

class NotionEntryRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Target Notion database ID")
    properties: Dict[str, Any] = Field(..., description="Properties to set (must match database schema)")
    content_blocks: Optional[List[Dict[str, Any]]] = Field(None, description="Optional list of Notion block children")

@router.post("/notion/create-database-entry")
def create_notion_database_entry(request: NotionEntryRequest):
    try:
        result = create_database_entry(
            notion_token=request.notion_token,
            database_id=request.database_id,
            properties=request.properties,
            content_blocks=request.content_blocks
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))