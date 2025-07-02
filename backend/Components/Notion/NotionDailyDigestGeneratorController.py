from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionDailyDigestGeneratorHelper import generate_notion_daily_digest

router = APIRouter()

class DailyDigestRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="ID of the Notion database")
    hours_back: int = Field(24, description="How many past hours to include in digest")
    max_items: int = Field(25, description="Max entries to include in digest")

@router.post("/notion/daily-digest")
def notion_daily_digest(request: DailyDigestRequest) -> Dict:
    try:
        return generate_notion_daily_digest(
            notion_token=request.notion_token,
            database_id=request.database_id,
            hours_back=request.hours_back,
            max_items=request.max_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))