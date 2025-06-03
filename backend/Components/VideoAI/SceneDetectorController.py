from fastapi import APIRouter, UploadFile, Form, HTTPException
from SceneDetectorHelper import detect_scenes
import os
import shutil
import cv2

router = APIRouter()

@router.post("/video/detect-scenes")
def detect_video_scenes(file: UploadFile, threshold: float = Form(30.0)):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        temp_path = os.path.join("temp_uploads", file.filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        scenes = detect_scenes(temp_path, threshold)

        cap = cv2.VideoCapture(temp_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        timestamps = [round(frame / fps, 2) for frame in scenes]

        os.remove(temp_path)
        return {
            "scene_frames": scenes,
            "scene_timestamps": timestamps,
            "count": len(scenes)
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))