from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
import shutil
from tempfile import NamedTemporaryFile
from BatchFileSplitterHelper import split_file_to_batches

app = FastAPI()

@app.post("/split/batch")
def api_split_file_to_batches(
    file: UploadFile = File(...),
    output_dir: str = Form(...),
    batch_size: int = Form(...),
    header: Optional[bool] = Form(True)
):
    try:
        with NamedTemporaryFile(delete=False, suffix=".csv") as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        output_files = split_file_to_batches(temp_path, output_dir, batch_size, header)
        return {"batches": output_files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
