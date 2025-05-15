from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import FileScannerHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    return True

class FileScannerRequest(BaseModel):
    file_path: str
    output_path: str
    scan_type: str = "default"
    scan_options: dict = {}
    algorithm: str = "sha256"
    
    def __init__(self, **data):
        super().__init__(**data)
        self.scan_options = {}

class FileScannerResponse(BaseModel):
    status: str
    data: dict = None
    error: str = None

@app.post("/FileScanner/file_hash")
async def get_file_hash(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    algorithm = form.get("algorithm", "sha256")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        hash_value = FileScannerHelper.get_file_hash(file_path, algorithm)
        with open(output_path, "w") as f:
            f.write(hash_value)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/FileScanner/mine_type")
async def get_mime_type(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        mime_type = FileScannerHelper.get_mime_type(file_path)
        with open(output_path, "w") as f:
            f.write(mime_type)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/extension")
async def get_file_extension(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        extension = FileScannerHelper.get_extension(file_path)
        with open(output_path, "w") as f:
            f.write(extension)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/is_executable")
async def is_executable(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        is_exec = FileScannerHelper.is_executable(file_path)
        with open(output_path, "w") as f:
            f.write(str(is_exec))
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/is_script_file")
async def is_script_file(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        is_script = FileScannerHelper.is_script_file(file_path)
        with open(output_path, "w") as f:
            f.write(str(is_script))
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/file_size")
async def get_file_size(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        size = FileScannerHelper.get_file_size(file_path)
        with open(output_path, "w") as f:
            f.write(str(size))
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/entropy")
async def get_entropy(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        entropy = FileScannerHelper.get_entropy(file_path)
        with open(output_path, "w") as f:
            f.write(str(entropy))
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/scan_with_yara")
async def scan_with_yara(request: FileScannerRequest, yara_rules_path: str):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    scan_type = form.get("scan_type", "default")
    scan_options = form.get("scan_options", {})
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        scan_result = FileScannerHelper.scan_with_yara(file_path, yara_rules_path)
        with open(output_path, "w") as f:
            f.write(scan_result)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/scan_with_virustotal")
async def scan_with_virustotal(request: FileScannerRequest, api_key: str):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        scan_result = FileScannerHelper.scan_with_virustotal(file_path, api_key)
        with open(output_path, "w") as f:
            f.write(scan_result)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/FileScanner/basic_scan")
async def basic_scan(request: FileScannerRequest):
    form = await request.form()
    file_path = form.get("file_path")
    output_path = form.get("output_path")
    
    validate_required_fields(form, ["file_path", "output_path"])

    try:
        scan_result = FileScannerHelper.basic_scan(file_path)
        with open(output_path, "w") as f:
            f.write(scan_result)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))