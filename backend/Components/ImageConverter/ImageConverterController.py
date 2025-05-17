from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from ImageConverterHelper import *

app = FastAPI()

UPLOAD_DIR = "temp_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_temp_file(upload_file: UploadFile) -> str:
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{upload_file.filename}")
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return temp_path

@app.post("/image/convert")
def api_convert_image_format(dest_path: str, file: UploadFile = File(...), dest_format: str = Form(...)):
    try:
        path = save_temp_file(file)
        output = convert_image_format(path, dest_format, dest_path)
        return {"converted_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image/resize")
def api_resize_image(dest_path: str, file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    try:
        path = save_temp_file(file)
        output = resize_image(path, width, height, dest_path)
        return {"resized_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image/compress")
def api_compress_image(dest_path: str, file: UploadFile = File(...), quality: int = Form(75)):
    try:
        path = save_temp_file(file)
        output = compress_image(path, quality, dest_path)
        return {"compressed_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image/crop")
def api_crop_image(dest_path: str, file: UploadFile = File(...), left: int = Form(...), top: int = Form(...), right: int = Form(...), bottom: int = Form(...)):
    try:
        path = save_temp_file(file)
        output = crop_image(path, (left, top, right, bottom), dest_path)
        return {"cropped_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image/rotate")
def api_rotate_image(dest_path: str, file: UploadFile = File(...), angle: float = Form(...)):
    try:
        path = save_temp_file(file)
        output = rotate_image(path, angle, dest_path)
        return {"rotated_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/image/grayscale")
def api_grayscale_image(dest_path: str, file: UploadFile = File(...)):
    try:
        path = save_temp_file(file)
        output = convert_to_grayscale(path, dest_path)
        return {"grayscale_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/image/thumbnail")
def api_thumbnail_image(dest_path: str, file: UploadFile = File(...), width: int = Form(128), height: int = Form(128)):
    try:
        path = save_temp_file(file)
        output = create_thumbnail(path, (width, height), dest_path)
        return {"thumbnail_path": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))