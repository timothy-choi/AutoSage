from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinPostDeleterHelper import delete_linkedin_post

router = APIRouter()

class LinkedInDeleteRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with delete permission")
    post_urn: str = Field(..., description="URN of the post to delete (e.g., 'urn:li:ugcPost:123456789')")

@router.delete("/linkedin/delete-post")
def delete_post(request: LinkedInDeleteRequest):
    result = delete_linkedin_post(
        access_token=request.access_token,
        post_urn=request.post_urn
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result)

    return result