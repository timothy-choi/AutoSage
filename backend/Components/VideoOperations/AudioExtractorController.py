from fastapi import APIRouter, UploadFile, HTTPException
from AudioExtractorHelper import extract_audio
import os
import uuid
import shutil

router = APIRouter()

@router.post("/video/extract-audio")
def extract_audio_from_video(file: UploadFile):
    try:
        temp_dir = "temp_audio"
        os.makedirs(temp_dir, exist_ok=True)
        temp_video_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_video_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        audio_path = extract_audio(temp_video_path)

        return {
            "message": "Audio extracted successfully",
            "audio_path": audio_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))