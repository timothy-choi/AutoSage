from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinPostPublisherHelper import publish_linkedin_post

router = APIRouter()

class LinkedInPostRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with permission to post")
    author_urn: str = Field(..., description="URN of the author (e.g., 'urn:li:person:...' or 'urn:li:organization:...')")
    post_text: str = Field(..., description="The message to post")
    visibility: str = Field(default="PUBLIC", description="Visibility setting: PUBLIC or CONNECTIONS")

@router.post("/linkedin/publish-post")
def publish_post(request: LinkedInPostRequest):
    result = publish_linkedin_post(
        access_token=request.access_token,
        author_urn=request.author_urn,
        post_text=request.post_text,
        visibility=request.visibility
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["details"])

    return result