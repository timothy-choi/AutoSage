from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from SummarizeContentHelper import summarize_content

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str
    num_sentences: int = 3

@router.post("/summarize")
def summarize_endpoint(request: SummarizeRequest):
    try:
        summary = summarize_content(request.text, request.num_sentences)
        if summary.startswith("Error"):
            raise HTTPException(status_code=400, detail=summary)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))