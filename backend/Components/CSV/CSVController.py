from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from typing import List, Optional
import shutil
import os
import uuid
from CSVHelper import *

app = FastAPI()

UPLOAD_DIR = "temp_csv"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_temp_file(upload_file: UploadFile) -> str:
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{upload_file.filename}")
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return temp_path

@app.post("/csv/read")
def api_read_csv(file: UploadFile = File(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        data = read_csv(path, delimiter)
        return {"rows": data}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/preview")
def api_preview_csv(file: UploadFile = File(...), num_rows: int = 5, delimiter: str = ","):
    try:
        path = save_temp_file(file)
        return {"preview": preview_csv(path, num_rows, delimiter)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/headers")
def api_get_headers(file: UploadFile = File(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        return {"headers": get_csv_headers(path, delimiter)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/filter")
def api_filter_csv(file: UploadFile = File(...), column: str = Query(...), value: str = Query(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        return {"filtered": filter_csv(path, column, value, delimiter)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/count")
def api_count_rows(file: UploadFile = File(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        return {"row_count": count_rows(path, delimiter)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/sort")
def api_sort_csv(file: UploadFile = File(...), column: str = Query(...), reverse: bool = False, delimiter: str = ","):
    try:
        path = save_temp_file(file)
        data = read_csv(path, delimiter)
        sorted_data = sort_csv(data, column, reverse)
        return {"sorted": sorted_data}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/deduplicate")
def api_deduplicate_csv(file: UploadFile = File(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        data = read_csv(path, delimiter)
        deduped_data = deduplicate_csv(data)
        return {"deduplicated": deduped_data}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@app.post("/csv/stats")
def api_column_stats(file: UploadFile = File(...), column: str = Query(...), delimiter: str = ","):
    try:
        path = save_temp_file(file)
        data = read_csv(path, delimiter)
        stats = column_stats(data, column)
        return {"stats": stats}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))