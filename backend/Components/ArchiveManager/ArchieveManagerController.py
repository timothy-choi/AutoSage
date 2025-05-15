from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import ArchieveManagerHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    return True

class ArchiveRequest(BaseModel):
    file_path: str
    output_path: str
    archive_format: str = "zip"
    compression_level: int = 5

class ArchiveResponse(BaseModel):
    status: str
    data: dict = None
    error: str = None

@app.post("/ArchiveManager/zip_files")
async def zip_files(request: ArchiveRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.zip_files(file_path, output_path)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))
    
@app.post("/ArchiveManager/unzip_files")
async def unzip_files(request: ArchiveRequest, zip_path: str, extract_to: str):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.unzip_file(zip_path, extract_to)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))
    
@app.post("/ArchiveManager/tar_files")
async def tar_files(request: ArchiveRequest, files: list[str], mode: str):
    form = await request.form()
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.tar_files(files, output_path, mode)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))
    
@app.post("/ArchiveManager/untar_files")
async def untar_files(request: ArchiveRequest, tar_path: str, extract_to: str):
    form = await request.form()
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.untar_file(tar_path, extract_to)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))
    
@app.post("/ArchiveManager/delete_files")
async def delete_files(request: ArchiveRequest, files: list[str]):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.delete_file(file_path)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))
    
@app.post("/ArchiveManager/rename_files")
async def rename_files(request: ArchiveRequest, original_path: str, new_path: str):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")

    validate_required_fields(form, ["file_path", "output_path"])

    try:
        data = ArchieveManagerHelper.rename_file(original_path, new_path)
        return ArchiveResponse(status="success", data=data)
    except Exception as e:
        return ArchiveResponse(status="error", error=str(e))