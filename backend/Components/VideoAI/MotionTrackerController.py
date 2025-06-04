from fastapi import APIRouter, UploadFile, HTTPException
from MotionTrackerHelper import track_motion
import os
import shutil
import uuid

router = APIRouter()

@router.post("/video/track-motion")
def track_motion_endpoint(file: UploadFile):
    try:
        temp_dir = "temp_motion"
        os.makedirs(temp_dir, exist_ok=True)

        video_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(video_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"motion_tracked_{os.path.basename(video_path)}")
        result_path = track_motion(video_path, output_path)

        return {
            "message": "Motion tracking completed",
            "output_path": result_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))