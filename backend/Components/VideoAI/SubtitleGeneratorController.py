from fastapi import APIRouter, UploadFile, File, HTTPException
from SubtitleGeneratorHelper import generate_subtitles_from_video
import os

router = APIRouter()

@router.post("/generate_subtitles")
def generate_subtitles_endpoint(video_file: UploadFile = File(...)):
    try:
        file_location = f"temp_{video_file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(video_file.file.read())

        subtitles_file = generate_subtitles_from_video(file_location)

        os.remove(file_location)

        return {"message": "Subtitles generated successfully", "subtitles_file": subtitles_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating subtitles: {str(e)}")