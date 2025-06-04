from fastapi import APIRouter, UploadFile, HTTPException
from VideoCombinerHelper import combine_videos
import os
import shutil
from typing import List
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/video/combine")
def combine_video_route(files: List[UploadFile]):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs", exist_ok=True)

        input_paths = []
        for file in files:
            file_path = os.path.join("temp_uploads", file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            input_paths.append(file_path)

        output_path = os.path.join("temp_outputs", "combined_video.mp4")
        combine_videos(input_paths, output_path)

        for path in input_paths:
            os.remove(path)

        return FileResponse(output_path, media_type="video/mp4", filename="combined_video.mp4")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="One or more video files not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))