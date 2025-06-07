from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import List, Optional
from DiscordSendMessageHelper import send_discord_message, send_embed, send_discord_file

router = APIRouter()

@router.post("/discord/send")
def post_discord_message(
    token: str = Query(...),
    channel_id: str = Query(...),
    message: str = Query(...),
    reply_to: Optional[str] = Query(None),
    mention_users: Optional[List[str]] = Query(None),
    mention_roles: Optional[List[str]] = Query(None),
    bold: bool = Query(False),
    italic: bool = Query(False),
    underline: bool = Query(False),
    code: bool = Query(False),
    preview: bool = Query(False)
):
    try:
        markdown_options = {"bold": bold, "italic": italic, "underline": underline, "code": code}
        result = send_discord_message(
            token, channel_id, message, reply_to, mention_users, mention_roles, markdown_options, preview
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/send/file")
def upload_file_message(
    token: str = Query(...),
    channel_id: str = Query(...),
    message: str = Query(""),
    file: UploadFile = File(...)
):
    try:
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        result = send_discord_file(token, channel_id, file_path, message)
        return {"status": "file_sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))