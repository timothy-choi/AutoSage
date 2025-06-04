from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoObjectDetectorHelper import detect_objects_in_video
import shutil
import os

router = APIRouter()

@router.post("/video/detect-objects")
def detect_objects(
    file: UploadFile,
    model_cfg: str = Form(...),
    model_weights: str = Form(...),
    labels_path: str = Form(...),
    confidence_threshold: float = Form(0.5)
):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        temp_path = os.path.join("temp_uploads", file.filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = detect_objects_in_video(
            video_path=temp_path,
            model_cfg=model_cfg,
            model_weights=model_weights,
            labels_path=labels_path,
            confidence_threshold=confidence_threshold
        )

        os.remove(temp_path)
        return {"detections": results, "frame_count": len(results)}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File or model files not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))