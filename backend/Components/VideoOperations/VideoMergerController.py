from fastapi import APIRouter, UploadFile, HTTPException, Query
from VideoMergerHelper import merge_videos
import os
import shutil
import uuid

router = APIRouter()

@router.post("/video/merge")
async def merge_uploaded_videos(
    files: list[UploadFile],
    crossfade: bool = Query(False),
    crossfade_duration: float = Query(1.0),
    resize_width: int = Query(None),
    resize_height: int = Query(None)
):
    try:
        temp_dir = "temp_merge"
        os.makedirs(temp_dir, exist_ok=True)

        video_paths = []
        for file in files:
            path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            video_paths.append(path)

        output_path = os.path.join(temp_dir, "merged_output.mp4")

        resize_to = (resize_width, resize_height) if resize_width and resize_height else None
        result_path = merge_videos(
            video_paths,
            output_path=output_path,
            with_crossfade=crossfade,
            crossfade_duration=crossfade_duration,
            resize_to=resize_to
        )

        return {
            "message": "Videos merged successfully",
            "output_path": result_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))