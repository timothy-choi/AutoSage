from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import DocxProcessorHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    
class DocxTextExtractionRequest(BaseModel):
    doc_path: str
    output_path: str
    font_name: str = "Helvetica"
    font_size: int = 12
    margin: int = 40
    line_spacing: int = 15

class DocxSplitRequest(BaseModel):
    doc_path: str
    output_dir: str
    output_files: list = []

    def __init__(self, **data):
        super().__init__(**data)
        self.output_files = []

class DocxMergeRequest(BaseModel):
    doc_paths: list
    output_path: str
    
    def __init__(self, **data):
        super().__init__(**data)
        self.output_path = ""

class DocxCreateFromTextRequest(BaseModel):
    text: str
    output_path: str
    font_name: str = "Helvetica"
    font_size: int = 12
    margin: int = 40
    line_spacing: int = 15

@app.post("/Docx/extractText")
def extract_text(request: DocxTextExtractionRequest):
    validate_required_fields(request, ["doc_path", "output_path"])
    
    try:
        text = DocxProcessorHelper.extract_text(request.doc_path)
        with open(request.output_path, "w") as f:
            f.write(text)
        return {"output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Docx/createDocxFromText")
def create_docx_from_text(request: DocxCreateFromTextRequest):
    validate_required_fields(request, ["text", "output_path"])
    
    try:
        DocxProcessorHelper.create_doc_from_text(request.text, request.output_path)
        return {"output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Docx/appendText")
def append_text(request: DocxTextExtractionRequest):
    validate_required_fields(request, ["doc_path", "text"])
    
    try:
        DocxProcessorHelper.append_text_to_doc(request.doc_path, request.text)
        return {"output_path": request.doc_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Docx/copy")
def copy_doc(request: DocxTextExtractionRequest):
    validate_required_fields(request, ["source_path", "destination_path"])
    
    try:
        DocxProcessorHelper.copy_doc(request.source_path, request.destination_path)
        return {"output_path": request.destination_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/Docx/rename")
def rename_doc(request: DocxTextExtractionRequest):
    validate_required_fields(request, ["original_path", "new_path"])
    
    try:
        DocxProcessorHelper.rename_doc(request.original_path, request.new_path)
        return {"output_path": request.new_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Docx/delete")
def delete_doc(request: DocxTextExtractionRequest):
    validate_required_fields(request, ["doc_path"])
    
    try:
        DocxProcessorHelper.delete_doc(request.doc_path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))