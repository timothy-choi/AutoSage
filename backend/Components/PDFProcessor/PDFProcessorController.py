from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import PDFProcessorHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    
class PDFTextExtractionRequest(BaseModel):
    pdf_path: str
    output_path: str
    font_name: str = "Helvetica"
    font_size: int = 12
    margin: int = 40
    line_spacing: int = 15

class PDFSplitRequest(BaseModel):
    pdf_path: str
    output_dir: str
    output_files: list = []

    def __init__(self, **data):
        super().__init__(**data)
        self.output_files = []

class PDFMergeRequest(BaseModel):
    pdf_paths: list
    output_path: str
    
    def __init__(self, **data):
        super().__init__(**data)
        self.output_path = ""

class PDFCreateFromTextRequest(BaseModel):
    text: str
    output_path: str
    font_name: str = "Helvetica"
    font_size: int = 12
    margin: int = 40
    line_spacing: int = 15

@app.post("/PDF/extractText")
def extract_text(request: PDFTextExtractionRequest):
    validate_required_fields(request, ["pdf_path", "output_path"])
    
    try:
        text = PDFProcessorHelper.extract_text(request.pdf_path)
        with open(request.output_path, "w") as f:
            f.write(text)
        return {"output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/PDF/split")
def split_pdf(request: PDFSplitRequest):
    validate_required_fields(request, ["pdf_path", "output_dir"])
    
    try:
        request.output_files = PDFProcessorHelper.split_pdf(request.pdf_path, request.output_dir)
        return {"output_files": request.output_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/PDF/merge")
def merge_pdfs(request: PDFMergeRequest):
    validate_required_fields(request, ["pdf_paths", "output_path"])
    
    try:
        request.output_path = PDFProcessorHelper.merge_pdfs(request.pdf_paths, request.output_path)
        return {"output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/PDF/createFromText")
def create_pdf_from_text(request: PDFCreateFromTextRequest):
    validate_required_fields(request, ["text", "output_path"])
    
    try:
        request.output_path = PDFProcessorHelper.create_pdf_from_text(
            request.text,
            request.output_path,
            request.font_name,
            request.font_size,
            request.margin,
            request.line_spacing
        )
        return {"output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/PDF/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return {"file_location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/PDF/download")
async def download_pdf(file_path: str):
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/PDF/encrypt")
def encrypt_pdf(pdf_path: str, password: str):
    validate_required_fields({"pdf_path": pdf_path, "password": password}, ["pdf_path", "password"])
    
    try:
        output_path = PDFProcessorHelper.encrypt_pdf(pdf_path, password)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/PDF/addWatermark")
def add_watermark(pdf_path: str, watermark_path: str, output_path: str):
    validate_required_fields({"pdf_path": pdf_path, "watermark_path": watermark_path, "output_path": output_path}, ["pdf_path", "watermark_path", "output_path"])
    
    try:
        output_path = PDFProcessorHelper.add_watermark(pdf_path, watermark_path, output_path)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/PDF/extractPages") 
def extract_pages(pdf_path: str, page_numbers: list, output_path: str):
    validate_required_fields({"pdf_path": pdf_path, "page_numbers": page_numbers, "output_path": output_path}, ["pdf_path", "page_numbers", "output_path"])
    
    try:
        output_path = PDFProcessorHelper.extract_pages(pdf_path, page_numbers, output_path)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))