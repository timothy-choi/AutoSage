from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import FileResponse
from PresignedURLHelper import *
import os

app = FastAPI()

@app.get("/generate")
def generate_url(base_url: str = Query(...), file_path: str = Query(...), expires_in: int = Query(3600)):
    try:
        url = generate_custom_presigned_url(base_url, file_path, expires_in)
        return {"presigned_url": url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/validate")
def validate_url(file: str = Query(...), expires: str = Query(...), signature: str = Query(...)):
    try:
        is_valid = validate_presigned_url(file, expires, signature)
        return {"valid": is_valid}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
def download_file(file: str = Query(...), expires: str = Query(...), signature: str = Query(...)):
    try:
        if not validate_presigned_url(file, expires, signature):
            raise HTTPException(status_code=403, detail="Invalid or expired signature")
        if not os.path.isfile(file):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file, filename=os.path.basename(file))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))