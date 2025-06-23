from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List
from LinkedinFollowerTrackerHelper import (
    track_linkedin_follower_changes,
    parse_follower_file
)

router = APIRouter()

class LinkedInFollowerTrackingRequest(BaseModel):
    old_followers: List[str] = Field(..., description="List of previous follower names or URNs")
    new_followers: List[str] = Field(..., description="List of current follower names or URNs")

@router.post("/linkedin/track-followers")
def track_followers(request: LinkedInFollowerTrackingRequest):
    if not request.old_followers or not request.new_followers:
        raise HTTPException(status_code=400, detail="Both old and new follower lists are required.")

    result = track_linkedin_follower_changes(
        old_followers=request.old_followers,
        new_followers=request.new_followers
    )
    return result

@router.post("/linkedin/track-followers/from-files")
async def track_followers_from_files(
    old_file: UploadFile = File(..., description="Old followers list (CSV or JSON)"),
    new_file: UploadFile = File(..., description="New followers list (CSV or JSON)")
):
    old_list = await parse_follower_file(old_file)
    new_list = await parse_follower_file(new_file)

    if not old_list or not new_list:
        raise HTTPException(status_code=400, detail="One or both files could not be parsed or were empty.")

    result = track_linkedin_follower_changes(old_list, new_list)
    return result