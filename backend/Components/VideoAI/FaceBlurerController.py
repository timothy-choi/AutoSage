from fastapi import APIRouter, UploadFile, HTTPException
from FaceBlurerHelper import blur_faces_in_video
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/video/blur-faces")
def blur_faces(file: UploadFile):
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("temp_outputs", exist_ok=True)

        input_path = os.path.join("temp_uploads", file.filename)
        output_path = os.path.join("temp_outputs", f"blurred_{file.filename}")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        blur_faces_in_video(input_path, output_path)
        os.remove(input_path)

        return FileResponse(output_path, media_type="video/mp4", filename=os.path.basename(output_path))

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))