from fastapi import APIRouter, Query, HTTPException
from TeamsAttachmentFetcherHelper import list_attachments_in_channel_message, download_attachment_by_url
from fastapi.responses import StreamingResponse
import io

router = APIRouter()


@router.get("/teams/attachments/list")
def get_attachments(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    message_id: str = Query(...)
):
    try:
        attachments = list_attachments_in_channel_message(access_token, team_id, channel_id, message_id)
        return {"attachments": attachments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/attachments/download")
def download_attachment(
    access_token: str = Query(...),
    url: str = Query(...),
    filename: str = Query("attachment.dat")
):
    try:
        file_bytes = download_attachment_by_url(access_token, url)
        return StreamingResponse(io.BytesIO(file_bytes), media_type="application/octet-stream", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))