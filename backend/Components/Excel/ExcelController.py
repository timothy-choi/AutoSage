from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import ExcelHelper

app = FastAPI()

def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    return True

class RequestExcel(BaseModel):
    file_path: str
    output_path: str
    sheet_name: str = None
    cell_range: str = None

class RequestExcelCreate(BaseModel):
    text: str
    output_path: str
    sheet_name: str = None
    cell_range: str = None

class RequestExcelAppend(BaseModel):
    file_path: str
    row_data: str

@app.post("/Excel/extractText")
async def extract_text(request: RequestExcel):
    form = await request.form()
    file = form.get("file")
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    output_path = form.get("output_path")
    if not output_path:
        raise HTTPException(status_code=400, detail="Output path is required")
    
    try:
        text = ExcelHelper.extract_text_from_excel(file.file)
        with open(output_path, "w") as f:
            f.write(text)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Excel/createExcelFromText")
async def create_excel_from_text(request: RequestExcelCreate):
    form = await request.form()
    text = form.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    output_path = form.get("output_path")
    if not output_path:
        raise HTTPException(status_code=400, detail="Output path is required")
    
    try:
        ExcelHelper.create_excel(text, output_path)
        return {"output_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Excel/readExcel")
async def read_excel(file_path: str):
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    try:
        data = ExcelHelper.read_excel(file_path)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Excel/appendRow")
async def append_row(request: RequestExcelAppend):
    file_path = request.query_params.get("file_path")
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    row_data = request.query_params.get("row_data")
    if not row_data:
        raise HTTPException(status_code=400, detail="Row data is required")
    
    try:
        ExcelHelper.append_row(file_path, row_data)
        return JSONResponse(content={"message": "Row appended successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Excel/cellValue")
async def cell_value(file_path: str, cell: str):
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    if not cell:
        raise HTTPException(status_code=400, detail="Cell is required")
    
    try:
        value = ExcelHelper.get_cell_value(file_path, cell)
        return JSONResponse(content={"value": value})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/Excel/setCellValue")
async def set_cell_value(file_path: str, cell: str, value: str):
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    if not cell:
        raise HTTPException(status_code=400, detail="Cell is required")
    
    if not value:
        raise HTTPException(status_code=400, detail="Value is required")
    
    try:
        ExcelHelper.set_cell_value(file_path, cell, value)
        return JSONResponse(content={"message": "Cell value set successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/Excel/deleteRow")
async def delete_row(file_path: str, row: int):
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    if row is None:
        raise HTTPException(status_code=400, detail="Row is required")
    
    try:
        ExcelHelper.delete_row(file_path, row)
        return JSONResponse(content={"message": "Row deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Excel/copy")
async def copy_excel(source_path: str, destination_path: str):
    if not source_path:
        raise HTTPException(status_code=400, detail="Source path is required")
    
    if not destination_path:
        raise HTTPException(status_code=400, detail="Destination path is required")
    
    try:
        ExcelHelper.copy_excel(source_path, destination_path)
        return JSONResponse(content={"message": "File copied successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/Excel/rename")
async def rename_excel(original_path: str, new_path: str):
    if not original_path:
        raise HTTPException(status_code=400, detail="Original path is required")
    
    if not new_path:
        raise HTTPException(status_code=400, detail="New path is required")
    
    try:
        ExcelHelper.rename_excel(original_path, new_path)
        return JSONResponse(content={"message": "File renamed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/Excel/delete")
async def delete_excel(file_path: str):
    if not file_path:
        raise HTTPException(status_code=400, detail="File path is required")
    
    try:
        ExcelHelper.delete_excel(file_path)
        return JSONResponse(content={"message": "File deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))