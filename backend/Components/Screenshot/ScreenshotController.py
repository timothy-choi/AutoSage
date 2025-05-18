from fastapi import FastAPI, Query, Response
from typing import Optional
from ScreenshotHelper import *

app = FastAPI()

@app.get("/screenshot")
def api_take_screenshot(filename: Optional[str] = None):
    try:
        path = take_screenshot(filename)
        return {"saved_to": path}
    except Exception as e:
        return {"error": str(e)}

@app.get("/screenshot/region")
def api_take_region_screenshot(
    left: int = Query(...),
    top: int = Query(...),
    width: int = Query(...),
    height: int = Query(...),
    filename: Optional[str] = None
):
    try:
        path = take_screenshot(filename, region=(left, top, width, height))
        return {"saved_to": path}
    except Exception as e:
        return {"error": str(e)}

@app.get("/screenshot/bytes")
def api_screenshot_bytes(
    left: Optional[int] = None,
    top: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None
):
    try:
        region = (left, top, width, height) if None not in (left, top, width, height) else None
        img_bytes = screenshot_to_bytes(region=region)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/screenshot/folder")
def api_save_to_folder(folder: Optional[str] = "screenshots"):
    try:
        path = save_screenshot_to_folder(folder)
        return {"saved_to": path}
    except Exception as e:
        return {"error": str(e)}