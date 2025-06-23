from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinContentSummarizerHelper import summarize_linkedin_content

router = APIRouter()

class LinkedInContentSummaryRequest(BaseModel):
    content: str = Field(..., description="Raw content from a LinkedIn post, article, or comment thread")
    tone: str = Field(default="professional", description="Summary tone (e.g., 'professional', 'casual')")
    length: str = Field(default="short", description="Summary length: short, medium, or detailed")

@router.post("/linkedin/summarize-content")
def summarize_content(request: LinkedInContentSummaryRequest):
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    summary = summarize_linkedin_content(
        content=request.content,
        tone=request.tone,
        length=request.length
    )

    return {"summary": summary}