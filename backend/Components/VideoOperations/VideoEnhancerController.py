from fastapi import APIRouter, UploadFile, HTTPException, Query
from VideoEnhancerHelper import enhance_video
import os
import uuid
import shutil

router = APIRouter()

@router.post("/video/enhance")
def enhance_uploaded_video(
    file: UploadFile,
    brightness: int = Query(30),
    contrast: int = Query(30)
):
    try:
        temp_dir = "temp_enhanced"
        os.makedirs(temp_dir, exist_ok=True)

        input_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"enhanced_{os.path.basename(input_path)}")
        enhanced_path = enhance_video(input_path, output_path, brightness, contrast)

        return {
            "message": "Video enhanced successfully",
            "output_path": enhanced_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
