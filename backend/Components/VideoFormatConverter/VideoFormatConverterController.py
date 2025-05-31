from fastapi import APIRouter, HTTPException, Query
from typing import List
import os
from VideoFormatConverterHelper import convert_video_format, extract_audio, batch_convert_format

router = APIRouter()

@router.post("/video/convert")
def convert_video(filename: str = Query(...), format: str = Query("mp4")):
    try:
        input_path = os.path.join("uploaded_videos", filename)
        result = convert_video_format(input_path, format)
        return {"message": "Conversion successful", "path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video/extract-audio")
def extract_video_audio(filename: str = Query(...)):
    try:
        input_path = os.path.join("uploaded_videos", filename)
        result = extract_audio(input_path)
        return {"message": "Audio extracted", "path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video/batch-convert")
def batch_convert_videos(filenames: List[str] = Query(...), format: str = Query("mp4")):
    try:
        paths = [os.path.join("uploaded_videos", f) for f in filenames]
        results = batch_convert_format(paths, format)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))