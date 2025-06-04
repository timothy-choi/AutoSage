from fastapi import APIRouter, UploadFile, HTTPException
from SubtitleEmbedderHelper import embed_subtitles
import shutil
import uuid
import os

router = APIRouter()

@router.post("/video/embed-subtitles")
def embed_subtitles_into_video(video_file: UploadFile, subtitle_file: UploadFile):
    try:
        temp_dir = "temp_subtitles"
        os.makedirs(temp_dir, exist_ok=True)

        video_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{video_file.filename}")
        subtitle_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{subtitle_file.filename}")

        with open(video_path, "wb") as v:
            shutil.copyfileobj(video_file.file, v)

        with open(subtitle_path, "wb") as s:
            shutil.copyfileobj(subtitle_file.file, s)

        output_path = embed_subtitles(video_path, subtitle_path)

        return {
            "message": "Subtitles embedded successfully",
            "output_path": output_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
