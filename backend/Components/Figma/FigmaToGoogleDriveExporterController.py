from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from FigmaToGoogleDriveExporterHelper import export_figma_to_drive

router = APIRouter()

class FigmaToDriveRequest(BaseModel):
    figma_token: str
    file_key: str
    node_ids: List[str]  
    format: str          
    service_account_json: str  
    folder_id: str      

@router.post("/figma/to-google-drive/export")
async def export_to_google_drive(req: FigmaToDriveRequest):
    return export_figma_to_drive(
        figma_token=req.figma_token,
        file_key=req.file_key,
        node_ids=req.node_ids,
        format=req.format,
        service_account_json=req.service_account_json,
        folder_id=req.folder_id
    )