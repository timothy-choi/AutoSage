from fastapi import APIRouter, UploadFile, Form, HTTPException
from VideoSummarizerHelper import summarize_video, extract_key_frames
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/video/summarize")
def summarize_video_route(file: UploadFile, method: str = Form("frame_skip"), frame_skip: int = Form(30), threshold: float = Form(30.0)):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs", exist_ok=True)

        input_path = os.path.join("temp_uploads", file.filename)
        output_path = os.path.join("temp_outputs", f"summary_{file.filename}")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if method == "frame_skip":
            summarize_video(input_path, output_path, frame_skip)
            os.remove(input_path)
            return FileResponse(output_path, media_type="video/mp4", filename=os.path.basename(output_path))

        elif method == "key_frames":
            timestamps = extract_key_frames(input_path, threshold)
            os.remove(input_path)
            return {"key_frame_timestamps": timestamps, "count": len(timestamps)}

        else:
            raise HTTPException(status_code=400, detail="Invalid summarization method")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))