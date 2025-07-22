from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from FigmaComponentUsageAnalyzerHelper import analyze_component_usage

router = APIRouter()

class FigmaUsageRequest(BaseModel):
    figma_token: str
    file_key: str

@router.post("/figma/component-usage/analyze")
async def analyze_usage(req: FigmaUsageRequest):
    return analyze_component_usage(req.figma_token, req.file_key)