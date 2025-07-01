from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionDatabaseSchemaFetcherHelper import fetch_database_schema

router = APIRouter()

class NotionSchemaRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="ID of the Notion database to inspect")

@router.post("/notion/fetch-database-schema")
def get_database_schema(request: NotionSchemaRequest):
    try:
        result = fetch_database_schema(
            notion_token=request.notion_token,
            database_id=request.database_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))