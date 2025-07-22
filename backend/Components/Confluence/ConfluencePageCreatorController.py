from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ConfluencePageCreatorHelper import create_confluence_page

router = APIRouter()

class ConfluencePageCreateRequest(BaseModel):
    base_url: str                 
    username: str                
    api_token: str                
    space_key: str               
    title: str
    content: str                 
    parent_id: Optional[str] = None  

@router.post("/confluence/page/create")
def create_page(req: ConfluencePageCreateRequest):
    try:
        page = create_confluence_page(
            req.base_url,
            req.username,
            req.api_token,
            req.space_key,
            req.title,
            req.content,
            req.parent_id
        )
        return {"status": "success", "page_id": page["id"], "link": page["_links"]["base"] + page["_links"]["webui"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))