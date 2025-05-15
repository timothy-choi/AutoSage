from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import CloudStorageHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    return True

class CloudStorageRequest(BaseModel):
    bucket_name: str
    file_path: str
    destination_path: str
    operation: str = "upload"
    metadata: dict = {}
    credentials_path: str = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self.metadata = {}

class CloudStorageResponse(BaseModel):
    status: str
    data: dict = None
    error: str = None

@app.post("/CloudStorage/drive/upload")
async def upload_file(request: CloudStorageRequest, folder_id: str = None):
    form = await request.form()
    bucket_name = form.get("bucket_name")
    file_path = form.get("file_path")
    destination_path = form.get("destination_path")
    credentials_path = form.get("credentials_path")

    validate_required_fields(form, ["bucket_name", "file_path", "destination_path"])

    try:
        CloudStorageHelper.configure_google_drive(credentials_path)

        data = CloudStorageHelper.upload_to_gdrive(file_path, folder_id)
        return CloudStorageResponse(status="success", data=data)
    except Exception as e:
        return CloudStorageResponse(status="error", error=str(e))

@app.post("/CloudStorage/drive/download")
async def download_file(request: CloudStorageRequest):
    form = await request.form()
    file_path = form.get("file_path")
    destination_path = form.get("destination_path")
    credentials_path = form.get("credentials_path")

    validate_required_fields(form, ["bucket_name", "file_path", "destination_path"])

    try:
        CloudStorageHelper.configure_google_drive(credentials_path)

        data = CloudStorageHelper.download_gdrive_file(file_path, destination_path)
        return CloudStorageResponse(status="success", data=data)
    except Exception as e:
        return CloudStorageResponse(status="error", error=str(e))
    
@app.post("/CloudStorage/drive/check_file_exists")
async def check_file_exists(request: CloudStorageRequest, file_id: str):
    form = await request.form()
    file_path = form.get("file_path")
    credentials_path = form.get("credentials_path")

    validate_required_fields(form, ["bucket_name", "file_path"])

    try:
        CloudStorageHelper.configure_google_drive(credentials_path)

        data = CloudStorageHelper.check_gdrive_file_exists(file_id)
        return CloudStorageResponse(status="success", data=data)
    except Exception as e:
        return CloudStorageResponse(status="error", error=str(e))
    
@app.post("/CloudStorage/drive/list")
async def list_files(request: CloudStorageRequest, folder_id: str = None):
    form = await request.form()
    bucket_name = form.get("bucket_name")
    credentials_path = form.get("credentials_path")

    validate_required_fields(form, ["bucket_name"])

    try:
        CloudStorageHelper.configure_google_drive(credentials_path)

        data = CloudStorageHelper.list_gdrive_files(folder_id)
        return CloudStorageResponse(status="success", data=data)
    except Exception as e:
        return CloudStorageResponse(status="error", error=str(e))
    
@app.post("/CloudStorage/drive/delete")
async def delete_file(request: CloudStorageRequest, file_id: str):
    form = await request.form()
    bucket_name = form.get("bucket_name")
    credentials_path = form.get("credentials_path")

    validate_required_fields(form, ["bucket_name", "file_id"])

    try:
        CloudStorageHelper.configure_google_drive(credentials_path)

        data = CloudStorageHelper.delete_gdrive_file(file_id)
        return CloudStorageResponse(status="success", data=data)
    except Exception as e:
        return CloudStorageResponse(status="error", error=str(e))