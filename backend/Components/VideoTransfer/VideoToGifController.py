from fastapi import APIRouter, UploadFile, HTTPException, Query
from VideoToGifConverterHelper import convert_video_to_gif
import os
import shutil
import uuid

router = APIRouter()

@router.post("/video/convert-to-gif")
def convert_to_gif(
    file: UploadFile,
    start_time: float = Query(0),
    end_time: float = Query(None),
    resize_width: int = Query(None),
    fps: int = Query(10)
):
    try:
        temp_dir = "temp_gif"
        os.makedirs(temp_dir, exist_ok=True)

        input_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.gif")
        gif_path = convert_video_to_gif(
            input_path=input_path,
            output_path=output_path,
            start_time=start_time,
            end_time=end_time,
            resize_width=resize_width,
            fps=fps
        )

        return {
            "message": "GIF created successfully",
            "gif_path": gif_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))