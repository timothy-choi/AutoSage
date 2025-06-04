from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoClassifierHelper import classify_video
import shutil
import os

router = APIRouter()

@router.post("/video/classify")
def classify_video_route(
    file: UploadFile,
    model_path: str = Form(...),
    labels_path: str = Form(...),
    frame_interval: int = Form(30)
):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        video_path = os.path.join("temp_uploads", file.filename)

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = classify_video(video_path, model_path, labels_path, frame_interval)

        os.remove(video_path)
        return {"classifications": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File or model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))