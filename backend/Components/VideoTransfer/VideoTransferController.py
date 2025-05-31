from fastapi import APIRouter, UploadFile, HTTPException, Query
from VideoTransferHelper import save_video, download_video, list_videos, delete_video
import os

router = APIRouter()

@router.post("/video/upload")
def upload_video(file: UploadFile):
    try:
        path = save_video(file)
        return {"message": "Upload successful", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video/download")
def fetch_video(url: str = Query(...), save_as: str = Query("downloaded_video.mp4")):
    try:
        path = download_video(url, os.path.join("downloaded_videos", save_as))
        return {"message": "Download successful", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/list")
def list_uploaded_videos():
    try:
        filenames = list_videos("uploaded_videos")
        return {"videos": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/video/delete")
def remove_video(filename: str = Query(...)):
    try:
        deleted = delete_video(filename, "uploaded_videos")
        return {"message": f"Deleted {deleted}"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))