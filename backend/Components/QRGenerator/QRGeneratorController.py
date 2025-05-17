from fastapi import FastAPI, Query, Response, HTTPException
from typing import Optional
import QRGeneratorHelper

app = FastAPI()

@app.get("/qr/basic")
def qr_basic(data: str, filename: Optional[str] = None):
    try:
        path = QRGeneratorHelper.generate_qr_code(data, filename)
        return {"saved_to": path}
    except Exception as e:
        return HTTPException(status_code=500)

@app.get("/qr/custom")
def qr_custom(data: str, filename: Optional[str] = None, box_size: int = 10, border: int = 4):
    try:
        path = QRGeneratorHelper.generate_custom_qr_code(data, filename, box_size, border)
        return {"saved_to": path}
    except Exception as e:
        return HTTPException(status_code=500)
    
@app.get("/qr/bytes")
def qr_bytes(data: str, box_size: int = 10, border: int = 4):
    try:
        img_bytes = QRGeneratorHelper.generate_qr_as_bytes(data, box_size, border)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        return HTTPException(status_code=500)
    
@app.get("/qr/url")
def qr_url(url: str, filename: Optional[str] = None):
    try:
        path = QRGeneratorHelper.generate_qr_from_url(url, filename)
        return {"saved_to": path}
    except Exception as e:
        return HTTPException(status_code=500)