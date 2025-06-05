from fastapi import APIRouter, UploadFile, HTTPException, Query
from VIdeoResizerHelper import resize_video
import shutil
import uuid
import os

router = APIRouter()

@router.post("/video/resize")
def resize_uploaded_video(
    file: UploadFile,
    width: int = Query(..., gt=0),
    height: int = Query(..., gt=0)
):
    try:
        temp_dir = "temp_resize"
        os.makedirs(temp_dir, exist_ok=True)

        input_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_path = os.path.join(temp_dir, f"resized_{os.path.basename(input_path)}")
        resized = resize_video(input_path, output_path, width, height)

        return {
            "message": "Video resized successfully",
            "output_path": resized
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))