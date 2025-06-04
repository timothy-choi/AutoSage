from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoTrimmerHelper import trim_video
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/video/trim")
def trim_video_route(
    file: UploadFile,
    start_time: float = Form(...),
    end_time: float = Form(...)
):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs", exist_ok=True)

        input_path = os.path.join("temp_uploads", file.filename)
        output_path = os.path.join("temp_outputs", f"trimmed_{file.filename}")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        trim_video(input_path, output_path, start_time, end_time)
        os.remove(input_path)

        return FileResponse(output_path, media_type="video/mp4", filename=os.path.basename(output_path))

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
