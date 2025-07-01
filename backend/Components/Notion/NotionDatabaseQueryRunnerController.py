from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from NotionDatabaseQueryRunnerHelper import query_notion_database

router = APIRouter()

class NotionQueryRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="The ID of the Notion database")
    filter_: Optional[Dict[str, Any]] = Field(None, description="Optional filter object")
    sorts: Optional[List[Dict[str, Any]]] = Field(None, description="Optional sorting options")
    page_size: Optional[int] = Field(10, description="Max number of results to return")

@router.post("/notion/query-database")
def query_notion_database_endpoint(request: NotionQueryRequest):
    try:
        result = query_notion_database(
            notion_token=request.notion_token,
            database_id=request.database_id,
            filter_=request.filter_,
            sorts=request.sorts,
            page_size=request.page_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))