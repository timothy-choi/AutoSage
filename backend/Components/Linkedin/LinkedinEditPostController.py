from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinEditPostHelper import edit_linkedin_post

router = APIRouter()

class LinkedInEditRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token")
    post_urn: str = Field(..., description="URN of the post to edit")
    author_urn: str = Field(..., description="URN of the author (user or organization)")
    new_content: str = Field(..., description="New content for the post")
    visibility: str = Field(default="PUBLIC", description="Post visibility")

@router.put("/linkedin/edit-post")
def edit_post(request: LinkedInEditRequest):
    result = edit_linkedin_post(
        access_token=request.access_token,
        post_urn=request.post_urn,
        author_urn=request.author_urn,
        new_content=request.new_content,
        visibility=request.visibility
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result)

    return result