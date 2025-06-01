from fastapi import APIRouter, Form, UploadFile, HTTPException
from YoutubeUploaderHelper import upload_video_to_youtube
import os
import shutil

router = APIRouter()

@router.post("/video/upload-youtube")
def upload_to_youtube(
    file: UploadFile,
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),  # comma-separated
    category_id: str = Form("22"),
    privacy_status: str = Form("unlisted")
):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        temp_path = os.path.join("temp_uploads", file.filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        result = upload_video_to_youtube(
            file_path=temp_path,
            title=title,
            description=description,
            tags=tag_list,
            category_id=category_id,
            privacy_status=privacy_status
        )

        os.remove(temp_path)
        return {"message": "Uploaded to YouTube", "response": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))