from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from GUIAutomatorHelper import *
import shutil
import os
import uuid
from typing import Optional

app = FastAPI()

UPLOAD_DIR = "temp_gui"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

@app.post("/gui/click")
def api_click(x: int = Form(...), y: int = Form(...), delay: float = Form(0.0)):
    try:
        click_at(x, y, delay)
        return {"status": "clicked"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/move")
def api_move(x: int = Form(...), y: int = Form(...), duration: float = Form(0.25)):
    try:
        move_mouse_to(x, y, duration)
        return {"status": "mouse moved"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/type")
def api_type(text: str = Form(...), interval: float = Form(0.05)):
    try:
        type_text(text, interval)
        return {"status": "text typed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/press")
def api_press(key: str = Form(...)):
    try:
        press_key(key)
        return {"status": "key pressed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/hotkey")
def api_hotkey(keys: str = Form(...)):
    try:
        hotkey(*keys.split(","))
        return {"status": "hotkey pressed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/screenshot")
def api_screenshot(left: Optional[int] = Form(None), top: Optional[int] = Form(None), width: Optional[int] = Form(None), height: Optional[int] = Form(None)):
    try:
        region = (left, top, width, height) if None not in (left, top, width, height) else None
        path = screenshot_region(region=region)
        return {"screenshot": path}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/gui/locate")
def api_locate(file: UploadFile = File(...), confidence: float = Form(0.8)):
    try:
        image_path = save_upload_file(file)
        location = locate_on_screen(image_path, confidence)
        return {"location": location}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})