from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ConfluencePageUpdaterHelper import update_confluence_page

router = APIRouter()

class ConfluencePageUpdateRequest(BaseModel):
    base_url: str                 
    username: str                 
    api_token: str                
    page_id: str                   
    new_title: str
    new_content: str             

@router.put("/confluence/page/update")
def update_page(req: ConfluencePageUpdateRequest):
    try:
        updated_page = update_confluence_page(
            req.base_url,
            req.username,
            req.api_token,
            req.page_id,
            req.new_title,
            req.new_content
        )
        return {
            "status": "success",
            "page_id": updated_page["id"],
            "link": updated_page["_links"]["base"] + updated_page["_links"]["webui"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))