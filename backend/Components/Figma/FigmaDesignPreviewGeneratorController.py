from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from FigmaDesignPreviewGeneratorHelper import generate_design_preview

router = APIRouter()

class FigmaDesignPreviewRequest(BaseModel):
    file_key: str
    access_token: str
    node_ids: Optional[List[str]] = None 
    format: Optional[str] = "png"
    scale: Optional[int] = 1

@router.post("/figma/preview-design")
def preview_design(request: FigmaDesignPreviewRequest):
    return generate_design_preview(
        file_key=request.file_key,
        access_token=request.access_token,
        node_ids=request.node_ids,
        format=request.format,
        scale=request.scale
    )