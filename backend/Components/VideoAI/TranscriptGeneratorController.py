from fastapi import APIRouter, UploadFile, HTTPException, Query
from TranscriptGeneratorHelper import generate_transcript
import os
import shutil
import uuid

router = APIRouter()

@router.post("/video/generate-transcript")
def generate_transcript_endpoint(file: UploadFile, model_size: str = Query("base"), save_to: str = Query("base"), format: str = Query("base")):
    try:
        temp_dir = "temp_transcript"
        os.makedirs(temp_dir, exist_ok=True)

        input_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = generate_transcript(input_path, model_size=model_size, save_to=save_to, format=format)

        return {
            "message": "Transcription completed",
            "transcript": result["text"],
            "segments": result["segments"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))