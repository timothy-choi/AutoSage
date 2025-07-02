from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionTemplateApplierController import apply_template_to_database

router = APIRouter()

class TemplateApplyRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    template_page_id: str = Field(..., description="Notion template page ID")
    target_database_id: str = Field(..., description="Target Notion database ID")

@router.post("/notion/apply-template")
def apply_template(request: TemplateApplyRequest):
    try:
        result = apply_template_to_database(
            notion_token=request.notion_token,
            template_page_id=request.template_page_id,
            database_id=request.target_database_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))