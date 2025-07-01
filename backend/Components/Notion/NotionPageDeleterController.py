from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionPageDeleterHelper import delete_notion_page

router = APIRouter()

class NotionPageDeleteRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    page_id: str = Field(..., description="The ID of the Notion page to archive/delete")

@router.delete("/notion/delete-page")
def delete_notion_page_endpoint(request: NotionPageDeleteRequest):
    try:
        result = delete_notion_page(request.notion_token, request.page_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))