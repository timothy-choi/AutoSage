from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse, Response
import AWSHelper as AWSHelpers

app = FastAPI()

class BucketInfo(BaseModel):
    bucket_name: str
    bucket_region: Optional[str] = None

class FileUploadInfo(BaseModel):
    bucket_name: str
    file_name: str
    file_body: str

class FileUploadFromPath(BaseModel):
    bucket_name: str
    file_path: str
    object_name: str

class FileDownloadInfo(BaseModel):
    bucket_name: str
    object_name: str
    local_file_path: str

class FileDownloadContentInfo(BaseModel):
    bucket_name: str
    object_name: str

class PresignedURLRequest(BaseModel):
    bucket_name: str
    key_name: str

@app.post("/AWS/createBucket")
def create_bucket(info: BucketInfo):
    if AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=409, detail="Bucket already exists")
    if not info.bucket_region:
        raise HTTPException(status_code=400, detail="Bucket region is missing")

    if AWSHelpers.create_bucket(info.bucket_name, info.bucket_region) == 1:
        raise HTTPException(status_code=409, detail="Can't create bucket")

    return {"bucket_name": info.bucket_name}

@app.put("/AWS/deleteBucket")
def delete_bucket(info: BucketInfo):
    if not AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket doesn't exist")

    if AWSHelpers.delete_bucket(info.bucket_name) == 1:
        raise HTTPException(status_code=409, detail="Can't delete bucket")

    return {"bucket_name": info.bucket_name}

@app.post("/AWS/uploadFile")
def upload_file(info: FileUploadInfo):
    if not AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket doesn't exist")

    if AWSHelpers.upload_data_to_s3(info.bucket_name, info.file_name, info.file_body) == 1:
        raise HTTPException(status_code=409, detail="Can't upload file")

    return {"file_name": info.file_name}

@app.post("/AWS/upload_file_from_path")
def upload_file_from_path(info: FileUploadFromPath):
    if not AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket doesn't exist")

    if AWSHelpers.upload_file_to_s3(info.bucket_name, info.object_name, info.file_path) == 1:
        raise HTTPException(status_code=409, detail="Can't upload file")

    return {"file_path": info.file_path}

@app.post("/AWS/downloadFile")
def download_file(info: FileDownloadInfo):
    if not AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket doesn't exist")

    if AWSHelpers.download_file_from_s3(info.bucket_name, info.object_name, info.local_file_path) == 1:
        raise HTTPException(status_code=409, detail="Can't download file")

    return {"object_name": info.object_name}

@app.post("/AWS/downloadContent")
def download_content(info: FileDownloadContentInfo):
    if not AWSHelpers.check_if_bucket_exists(info.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket doesn't exist")

    content = AWSHelpers.download_content_from_s3(info.bucket_name, info.object_name)
    return Response(content)

@app.post("/AWS/presignedUrl")
def generate_presigned_url(info: PresignedURLRequest):
    url = AWSHelpers.generate_presigned_url(info.bucket_name, info.key_name)
    return {"url": url}
