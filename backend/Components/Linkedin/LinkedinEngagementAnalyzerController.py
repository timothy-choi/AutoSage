from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Literal
from LinkedinEngagementAnalyzerHelper import (
    analyze_linkedin_engagement,
    fetch_linkedin_posts
)

router = APIRouter()

class LinkedInPost(BaseModel):
    content: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    impressions: Optional[int] = 0

class LinkedInFetchRequest(BaseModel):
    access_token: str
    entity_urn: str 
    entity_type: Literal["user", "organization"] = "user"
    count: int = 10

@router.post("/linkedin/analyze-engagement")
def analyze_engagement(posts: List[LinkedInPost]):
    if not posts:
        raise HTTPException(status_code=400, detail="No posts submitted.")
    result = analyze_linkedin_engagement([post.dict() for post in posts])
    return result

@router.post("/linkedin/fetch-and-analyze")
def fetch_and_analyze(request: LinkedInFetchRequest):
    posts = fetch_linkedin_posts(
        access_token=request.access_token,
        entity_urn=request.entity_urn,
        entity_type=request.entity_type,
        count=request.count
    )

    if isinstance(posts, dict) and "error" in posts:
        raise HTTPException(status_code=500, detail=posts["error"])

    result = analyze_linkedin_engagement(posts)
    return result