from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from NotionPageEditorHelper import edit_notion_page

router = APIRouter()

class NotionPageEditRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    page_id: str = Field(..., description="Notion page ID to update")
    title: Optional[str] = Field(None, description="New title for the page")
    tags: Optional[List[str]] = Field(None, description="New tags to apply")
    content: Optional[str] = Field(None, description="Paragraph content to append or update")

@router.patch("/notion/edit-page")
def edit_notion_page_endpoint(request: NotionPageEditRequest):
    try:
        result = edit_notion_page(
            notion_token=request.notion_token,
            page_id=request.page_id,
            title=request.title,
            tags=request.tags,
            content=request.content
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))