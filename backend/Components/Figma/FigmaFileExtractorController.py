from fastapi import APIRouter
from pydantic import BaseModel
from FigmaFileExtractorHelper import extract_figma_styles

router = APIRouter()

class FigmaStyleExtractRequest(BaseModel):
    file_key: str
    access_token: str

@router.post("/figma/extract-styles")
def extract_styles(request: FigmaStyleExtractRequest):
    return extract_figma_styles(request.file_key, request.access_token)