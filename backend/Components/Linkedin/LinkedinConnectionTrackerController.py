from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List
from LinkedinConnectionTrackerHelper import (
    track_linkedin_connection_changes,
    parse_connection_file
)

router = APIRouter()

class LinkedInConnectionTrackingRequest(BaseModel):
    old_connections: List[str] = Field(..., description="Previous LinkedIn connections (names or URNs)")
    new_connections: List[str] = Field(..., description="Current LinkedIn connections (names or URNs)")

@router.post("/linkedin/track-connections")
def track_connections(request: LinkedInConnectionTrackingRequest):
    if not request.old_connections or not request.new_connections:
        raise HTTPException(status_code=400, detail="Both old and new connection lists are required.")

    result = track_linkedin_connection_changes(
        old_connections=request.old_connections,
        new_connections=request.new_connections
    )
    return result

@router.post("/linkedin/track-connections/from-files")
async def track_connections_from_files(
    old_file: UploadFile = File(..., description="Old connections CSV or JSON"),
    new_file: UploadFile = File(..., description="New connections CSV or JSON")
):
    old_list = await parse_connection_file(old_file)
    new_list = await parse_connection_file(new_file)

    if not old_list or not new_list:
        raise HTTPException(status_code=400, detail="One or both files could not be parsed or were empty.")

    result = track_linkedin_connection_changes(
        old_connections=old_list,
        new_connections=new_list
    )
    return result