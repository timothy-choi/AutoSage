from fastapi import APIRouter, Query, Response
from ConfluenceAttachmentDownloaderHelper import download_confluence_attachment

router = APIRouter()

@router.get("/confluence/download-attachment")
async def download_attachment(
    page_id: str = Query(...),
    filename: str = Query(...)
):
    try:
        file_data = await download_confluence_attachment(page_id, filename)
        return Response(
            content=file_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}