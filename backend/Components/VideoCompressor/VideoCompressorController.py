from fastapi import APIRouter, HTTPException, Query
from typing import List
import os
from VideoCompressorHelper import compress_video, batch_compress_videos, estimate_compression

router = APIRouter()

@router.post("/video/compress")
def compress_single_video(filename: str = Query(...), crf: int = Query(28), preset: str = Query("medium")):
    try:
        input_path = os.path.join("uploaded_videos", filename)
        result = compress_video(input_path, crf=crf, preset=preset)
        return {"message": "Compression successful", "path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video/batch-compress")
def compress_multiple_videos(filenames: List[str] = Query(...), crf: int = Query(28), preset: str = Query("medium")):
    try:
        paths = [os.path.join("uploaded_videos", f) for f in filenames]
        results = batch_compress_videos(paths, crf=crf, preset=preset)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/estimate-compression")
def get_compression_estimate(filename: str = Query(...)):
    try:
        input_path = os.path.join("uploaded_videos", filename)
        estimate = estimate_compression(input_path)
        return estimate
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))