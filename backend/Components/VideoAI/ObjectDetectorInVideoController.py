from fastapi import APIRouter, UploadFile, HTTPException, Form
from ObjectDetectorInVideoHelper import detect_objects_in_video
import shutil
import uuid
import os

router = APIRouter()

@router.post("/video/detect-objects")
def detect_objects(
    video_file: UploadFile,
    config_file: UploadFile,
    weights_file: UploadFile,
    names_file: UploadFile,
    confidence: float = Form(0.5),
    nms: float = Form(0.4)
):
    try:
        temp_dir = "temp_yolo"
        os.makedirs(temp_dir, exist_ok=True)

        def save_temp(file: UploadFile) -> str:
            path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            return path

        video_path = save_temp(video_file)
        cfg_path = save_temp(config_file)
        weights_path = save_temp(weights_file)
        names_path = save_temp(names_file)

        result = detect_objects_in_video(video_path, cfg_path, weights_path, names_path, confidence, nms)

        return {
            "message": "Object detection completed",
            "frames_detected": len(result),
            "detections": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))