import requests
import os
import shutil
import glob
from fastapi import UploadFile

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