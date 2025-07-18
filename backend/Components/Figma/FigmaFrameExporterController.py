from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from FigmaFrameExporterHelper import export_figma_frames

router = APIRouter()

class FigmaFrameExportRequest(BaseModel):
    file_key: str
    frame_ids: List[str]
    access_token: str
    format: Optional[str] = "png"
    scale: Optional[int] = 1

@router.post("/figma/export-frames")
def export_frames(request: FigmaFrameExportRequest):
    return export_figma_frames(
        file_key=request.file_key,
        frame_ids=request.frame_ids,
        access_token=request.access_token,
        format=request.format,
        scale=request.scale
    )