from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramArchiveExporterHelper import export_user_media_archive

router = APIRouter()

class ArchiveExportRequest(BaseModel):
    user_id: str
    access_token: str

@router.post("/instagram/export-archive")
async def export_archive(req: ArchiveExportRequest):
    result = await export_user_media_archive(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result