from fastapi import APIRouter, UploadFile, HTTPException, Query
from FrameExtractorHelper import extract_frames
import shutil
import os
import uuid

router = APIRouter()

@router.post("/video/extract-frames")
def extract_video_frames(file: UploadFile, interval: int = Query(30)):
    try:
        temp_dir = "temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        temp_video_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")

        with open(temp_video_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        frame_output_dir = os.path.join(temp_dir, os.path.splitext(file.filename)[0])
        paths = extract_frames(temp_video_path, frame_output_dir, interval=interval)

        return {
            "message": f"{len(paths)} frames extracted",
            "frames": paths
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))