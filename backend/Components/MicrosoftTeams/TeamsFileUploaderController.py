from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from TeamsFileUploaderHelper import upload_file_to_channel

router = APIRouter()

@router.post("/teams/upload")
def upload_teams_file(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    file: UploadFile = File(...)
):
    try:
        file_bytes = file.file.read()
        result = upload_file_to_channel(
            access_token=access_token,
            team_id=team_id,
            channel_id=channel_id,
            file_name=file.filename,
            file_bytes=file_bytes
        )
        return {
            "status": "uploaded",
            "file_name": result.get("name"),
            "web_url": result.get("webUrl")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))