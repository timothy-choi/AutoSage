from fastapi import APIRouter
from pydantic import BaseModel
from FigmaContentAnalyzerHelper import analyze_figma_content

router = APIRouter()

class FigmaContentAnalyzerRequest(BaseModel):
    file_key: str
    access_token: str

@router.post("/figma/content-analyzer")
def analyze_content(request: FigmaContentAnalyzerRequest):
    return analyze_figma_content(
        file_key=request.file_key,
        access_token=request.access_token
    )