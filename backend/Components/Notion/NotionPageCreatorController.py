from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from NotionPageCreatorHelper import create_notion_page

router = APIRouter()

class NotionPageRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Notion database ID")
    title: str = Field(..., description="Title of the page")
    content: Optional[str] = Field(None, description="Optional paragraph content")
    tags: Optional[List[str]] = Field(None, description="Optional list of tags")

@router.post("/notion/create-page")
def create_notion_page_endpoint(request: NotionPageRequest):
    try:
        result = create_notion_page(
            notion_token=request.notion_token,
            database_id=request.database_id,
            title=request.title,
            content=request.content,
            tags=request.tags
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))