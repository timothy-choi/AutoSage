from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoSplitterHelper import split_video
import os
import shutil
from fastapi.responses import FileResponse, JSONResponse
from typing import List

router = APIRouter()

@router.post("/video/split")
def split_video_route(file: UploadFile, chunk_duration: float = Form(...)):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs/split", exist_ok=True)

        input_path = os.path.join("temp_uploads", file.filename)
        output_dir = os.path.join("temp_outputs", "split")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunk_paths = split_video(input_path, output_dir, chunk_duration)

        os.remove(input_path)
        filenames = [os.path.basename(path) for path in chunk_paths]

        return JSONResponse(content={"chunks": filenames})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))