from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinPostInsightsHelper import fetch_linkedin_post_insights

router = APIRouter()

class LinkedInInsightRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token")
    post_urn: str = Field(..., description="URN of the post, e.g. 'urn:li:ugcPost:123456789'")

@router.post("/linkedin/fetch-insights")
def fetch_insights(request: LinkedInInsightRequest):
    result = fetch_linkedin_post_insights(
        access_token=request.access_token,
        post_urn=request.post_urn
    )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result