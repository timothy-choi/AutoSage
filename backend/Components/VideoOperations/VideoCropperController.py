from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoCropperHelper import crop_video
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/video/crop")
def crop_video_route(
    file: UploadFile,
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...)
):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs", exist_ok=True)

        input_path = os.path.join("temp_uploads", file.filename)
        output_path = os.path.join("temp_outputs", f"cropped_{file.filename}")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        crop_video(input_path, output_path, x, y, width, height)
        os.remove(input_path)

        return FileResponse(output_path, media_type="video/mp4", filename=os.path.basename(output_path))

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))