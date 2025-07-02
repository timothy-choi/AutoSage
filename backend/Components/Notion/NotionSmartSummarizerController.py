from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionSmartSummarizerHelper import generate_notion_summary

router = APIRouter()

class NotionSummaryRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    page_id: str = Field(..., description="ID of the Notion page to summarize")
    openai_api_key: str = Field(..., description="API key for OpenAI summarization")

@router.post("/notion/summarize")
def summarize_notion_page(request: NotionSummaryRequest):
    result = generate_notion_summary(
        notion_token=request.notion_token,
        page_id=request.page_id,
        openai_api_key=request.openai_api_key
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result