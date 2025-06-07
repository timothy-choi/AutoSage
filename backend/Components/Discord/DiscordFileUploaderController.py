from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from DiscordFileUploaderHelper import upload_file_to_discord

router = APIRouter()

@router.post("/discord/upload/file")
def send_discord_file(
    token: str = Query(..., description="Bot token (prefixed with 'Bot ')"),
    channel_id: str = Query(..., description="Target channel ID"),
    message: str = Query("", description="Optional message"),
    file: UploadFile = File(...)
):
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f_out:
            f_out.write(file.file.read())

        result = upload_file_to_discord(token, channel_id, temp_path, message)
        return {"status": "success", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))