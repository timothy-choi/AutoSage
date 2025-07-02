from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionPropertyStatsAggregatorHelper import aggregate_property_counts

router = APIRouter()

class PropertyStatsRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="Notion database ID")
    property_name: str = Field(..., description="Property to aggregate (e.g., 'Status')")
    max_pages: int = Field(100, description="Max pages to scan")

@router.post("/notion/property-stats")
def notion_property_stats(request: PropertyStatsRequest) -> Dict:
    try:
        return aggregate_property_counts(
            notion_token=request.notion_token,
            database_id=request.database_id,
            property_name=request.property_name,
            max_pages=request.max_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))