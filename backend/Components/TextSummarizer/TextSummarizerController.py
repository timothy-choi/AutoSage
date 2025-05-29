from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from TextSummarizerHelper import summarize_text, summarize_paragraphs, summarize_file
import tempfile

app = FastAPI()

class TextInput(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 40

class ParagraphsInput(BaseModel):
    paragraphs: List[str]
    max_length: int = 100

@app.post("/summarize/text")
def summarize_text_endpoint(data: TextInput):
    try:
        summary = summarize_text(data.text, data.max_length, data.min_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/paragraphs")
def summarize_paragraphs_endpoint(data: ParagraphsInput):
    try:
        summary = summarize_paragraphs(data.paragraphs, data.max_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/file")
async def summarize_file_endpoint(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        summary = summarize_file(tmp_path)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))