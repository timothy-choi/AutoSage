from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
from OCRManagerHelper import *
import shutil
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "temp_ocr"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

@app.post("/ocr/text")
def api_extract_text(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        path = save_upload_file(file)
        text = extract_text_from_image(path, lang)
        return {"text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/bytes")
def api_extract_text_from_bytes(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        content = file.file.read()
        text = extract_text_from_bytes(content, lang)
        return {"text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/data")
def api_get_text_data(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        path = save_upload_file(file)
        data = get_text_data(path, lang)
        return {"results": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/boxed")
def api_get_image_with_boxes(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        path = save_upload_file(file)
        boxed_path = f"{path}_boxed.png"
        result = get_image_with_boxes(path, lang, boxed_path)
        if result and os.path.isfile(result):
            return FileResponse(result, media_type="image/png")
        return JSONResponse(status_code=404, content={"error": "Boxed image not created"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/confidence")
def api_get_words_with_confidence(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        path = save_upload_file(file)
        data = get_words_with_confidence(path, lang)
        return {"words": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/digits")
def api_extract_digits(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        path = save_upload_file(file)
        digits = extract_digits(path, lang)
        return {"digits": digits}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/orientation")
def api_detect_orientation(file: UploadFile = File(...)):
    try:
        path = save_upload_file(file)
        orientation = detect_orientation(path)
        return {"orientation": orientation}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})