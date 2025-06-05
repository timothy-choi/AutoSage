from fastapi import APIRouter, UploadFile, Form, HTTPException
from SlackFileUploaderHelper import upload_slack_file
import os
import uuid
import shutil

router = APIRouter()

@router.post("/slack/upload-file")
async def upload_file_to_slack(
    token: str = Form(...),
    channel: str = Form(...),
    title: str = Form(None),
    file: UploadFile = Form(...)
):
    try:
        temp_dir = "temp_slack_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = upload_slack_file(token, channel, file_path, title)

        os.remove(file_path)

        if not result.get("ok"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {
            "message": "File uploaded successfully",
            "response": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))