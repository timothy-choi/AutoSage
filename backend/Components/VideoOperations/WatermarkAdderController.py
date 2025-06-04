from fastapi import APIRouter, UploadFile, HTTPException, Query
from WatermarkAdderHelper import add_watermark
import os
import uuid
import shutil

router = APIRouter()

@router.post("/video/watermark")
def add_video_watermark(
    file: UploadFile,
    text: str = Query("Sample Watermark"),
    x: int = Query(30),
    y: int = Query(30),
    font_scale: float = Query(1.0),
    thickness: int = Query(2)
):
    try:
        temp_dir = "temp_watermarked"
        os.makedirs(temp_dir, exist_ok=True)

        temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"watermarked_{os.path.basename(temp_path)}")
        result_path = add_watermark(
            video_path=temp_path,
            output_path=output_path,
            watermark_text=text,
            position=(x, y),
            font_scale=font_scale,
            font_thickness=thickness
        )

        return {
            "message": "Watermark added successfully",
            "output_path": result_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))