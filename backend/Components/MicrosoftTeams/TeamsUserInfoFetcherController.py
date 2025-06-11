from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsUserInfoFetcherHelper import (
    fetch_teams_user_info,
    fetch_user_presence,
    fetch_user_photo,
    fetch_user_groups,
    search_users_by_email
)

router = APIRouter()

class UserInfoRequest(BaseModel):
    user_id: str
    access_token: str

class EmailLookupRequest(BaseModel):
    email: str
    access_token: str

@router.post("/teams/fetch-user-info")
async def fetch_user_info(req: UserInfoRequest):
    result = await fetch_teams_user_info(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/fetch-user-presence")
async def fetch_user_presence_api(req: UserInfoRequest):
    result = await fetch_user_presence(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/fetch-user-photo")
async def fetch_user_photo_api(req: UserInfoRequest):
    result = await fetch_user_photo(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/fetch-user-groups")
async def fetch_user_groups_api(req: UserInfoRequest):
    result = await fetch_user_groups(req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/search-user-by-email")
async def search_user_by_email_api(req: EmailLookupRequest):
    result = await search_users_by_email(req.email, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result