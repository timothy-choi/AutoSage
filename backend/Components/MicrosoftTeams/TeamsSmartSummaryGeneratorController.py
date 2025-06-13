from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsSmartSummaryGeneratorHelper import (
    generate_smart_summary,
    generate_action_items
)

router = APIRouter()

class SummaryRequest(BaseModel):
    text: str
    context: str = "team discussion"

@router.post("/teams/generate-summary")
async def generate_summary(req: SummaryRequest):
    result = await generate_smart_summary(req.text, req.context)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/teams/generate-action-items")
async def generate_actions(req: SummaryRequest):
    result = await generate_action_items(req.text, req.context)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result