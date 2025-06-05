from fastapi import APIRouter, UploadFile, HTTPException, Form
from typing import List
import os
import uuid
import shutil
import json

from DataPackageBuilderHelper import build_data_package

router = APIRouter()

@router.post("/package/data")
async def create_data_package(
    files: List[UploadFile],
    metadata_json: str = Form(...)
):
    try:
        metadata = json.loads(metadata_json)
        temp_dir = f"temp_data_{uuid.uuid4()}"
        os.makedirs(temp_dir, exist_ok=True)

        file_paths = []
        for file in files:
            dest_path = os.path.join(temp_dir, file.filename)
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(dest_path)

        zip_path = build_data_package(file_paths, metadata)
        shutil.rmtree(temp_dir)

        return {
            "message": "Data package created",
            "zip_file": zip_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))