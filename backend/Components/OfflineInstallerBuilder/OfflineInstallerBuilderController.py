from fastapi import APIRouter, UploadFile, HTTPException
from OfflineInstallerBuilderHelper import build_offline_installer
import os
import shutil
import uuid

router = APIRouter()

@router.post("/builder/offline-installer")
async def build_installer(script: UploadFile, requirements: UploadFile):
    try:
        temp_dir = f"temp_offline_{uuid.uuid4()}"
        os.makedirs(temp_dir, exist_ok=True)

        script_path = os.path.join(temp_dir, script.filename)
        requirements_path = os.path.join(temp_dir, requirements.filename)

        with open(script_path, "wb") as f:
            shutil.copyfileobj(script.file, f)
        with open(requirements_path, "wb") as f:
            shutil.copyfileobj(requirements.file, f)

        zip_path = build_offline_installer(script_path, requirements_path)
        return {
            "message": "Offline installer built successfully.",
            "zip_file": zip_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))