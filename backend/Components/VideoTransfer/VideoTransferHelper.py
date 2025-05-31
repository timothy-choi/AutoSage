import requests
import os
import shutil
import glob
from fastapi import UploadFile
import zipfile
import cv2
from typing import List


UPLOAD_DIR = "uploaded_videos"
DOWNLOAD_DIR = "downloaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url: str, save_path: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return save_path
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def save_video(file: UploadFile, filename: str = None) -> str:
    try:
        if filename is None:
            filename = file.filename
        save_path = os.path.join(UPLOAD_DIR, filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return save_path
    except Exception as e:
        raise Exception(f"Failed to save video: {str(e)}")

def list_videos(directory: str = UPLOAD_DIR) -> list:
    try:
        return [os.path.basename(f) for f in glob.glob(f"{directory}/*") if os.path.isfile(f)]
    except Exception as e:
        raise Exception(f"Failed to list videos: {str(e)}")

def delete_video(filename: str, directory: str = UPLOAD_DIR) -> str:
    try:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            os.remove(path)
            return filename
        raise FileNotFoundError("File not found")
    except Exception as e:
        raise Exception(f"Failed to delete video: {str(e)}")
    
def archive_videos(video_paths: List[str], archive_path: str = "video_archive.zip") -> str:
    try:
        with zipfile.ZipFile(archive_path, 'w') as zipf:
            for path in video_paths:
                if os.path.isfile(path):
                    zipf.write(path, arcname=os.path.basename(path))
        return archive_path
    except Exception as e:
        raise Exception(f"Failed to archive videos: {str(e)}")

def get_video_metadata(video_path: str) -> dict:
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Cannot open video file")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps else 0

        cap.release()
        return {
            "duration_seconds": duration,
            "fps": fps,
            "resolution": f"{width}x{height}",
            "frame_count": frame_count
        }
    except Exception as e:
        raise Exception(f"Failed to get video metadata: {str(e)}")

def rename_video(original_path: str, new_name: str) -> str:
    try:
        directory = os.path.dirname(original_path)
        new_path = os.path.join(directory, new_name)
        os.rename(original_path, new_path)
        return new_path
    except Exception as e:
        raise Exception(f"Failed to rename video: {str(e)}")

def move_video(source_path: str, destination_folder: str) -> str:
    try:
        os.makedirs(destination_folder, exist_ok=True)
        destination_path = os.path.join(destination_folder, os.path.basename(source_path))
        shutil.move(source_path, destination_path)
        return destination_path
    except Exception as e:
        raise Exception(f"Failed to move video: {str(e)}")