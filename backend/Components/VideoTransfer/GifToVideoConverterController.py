from fastapi import APIRouter, UploadFile, HTTPException, Query
from GifToVideoConverterHelper import convert_gif_to_video
import os
import shutil
import uuid

router = APIRouter()

@router.post("/gif/convert-to-video")
def convert_gif_to_video_endpoint(
    file: UploadFile,
    fps: int = Query(24)
):
    try:
        temp_dir = "temp_gif_to_video"
        os.makedirs(temp_dir, exist_ok=True)

        gif_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(gif_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp4")
        result_path = convert_gif_to_video(gif_path, output_path=output_path, fps=fps)

        return {
            "message": "GIF converted to video successfully",
            "video_path": result_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))