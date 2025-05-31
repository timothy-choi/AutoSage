from fastapi import APIRouter, UploadFile, HTTPException, Query
from VideoTransferHelper import save_video, download_video, list_videos, delete_video, archive_videos, get_video_metadata, rename_video, move_video
import os
from typing import List

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
    
@router.post("/video/archive")
def archive_selected_videos(files: List[str] = Query(...)):
    try:
        file_paths = [os.path.join("uploaded_videos", f) for f in files]
        archive_path = archive_videos(file_paths)
        return {"message": "Archive created", "archive_path": archive_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/metadata")
def fetch_video_metadata(filename: str = Query(...)):
    try:
        video_path = os.path.join("uploaded_videos", filename)
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Video not found")
        metadata = get_video_metadata(video_path)
        return metadata
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/video/rename")
def rename_video_file(old_name: str = Query(...), new_name: str = Query(...)):
    try:
        old_path = os.path.join("uploaded_videos", old_name)
        new_path = rename_video(old_path, new_name)
        return {"message": f"Renamed to {os.path.basename(new_path)}", "new_path": new_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/video/move")
def move_video_file(filename: str = Query(...), destination: str = Query("archived_videos")):
    try:
        source_path = os.path.join("uploaded_videos", filename)
        moved_path = move_video(source_path, destination)
        return {"message": f"Moved to {moved_path}", "path": moved_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))