from fastapi import APIRouter, Query
from BoxFilePreviewerHelper import preview_file

router = APIRouter()

@router.get("/box/files/preview")
def preview_box_file(
    file_id: str = Query(..., description="ID of the Box file to preview"),
    access_token: str = Query(..., description="Box API access token")
):
    return preview_file(file_id, access_token)