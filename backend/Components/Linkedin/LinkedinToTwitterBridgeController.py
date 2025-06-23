from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from LinkedinToTwitterBridgeHelper import forward_linkedin_post_to_twitter

router = APIRouter()

class LinkedInPostPayload(BaseModel):
    content: str = Field(..., description="Text content of the LinkedIn post to forward")

@router.post("/linkedin/bridge-to-twitter")
def bridge_to_twitter(payload: LinkedInPostPayload):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="LinkedIn content cannot be empty.")

    result = forward_linkedin_post_to_twitter(payload.content)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result