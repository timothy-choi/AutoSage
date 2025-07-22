from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ConfluencePageMoverHelper import move_confluence_page

router = APIRouter()

class ConfluencePageMoveRequest(BaseModel):
    base_url: str              
    username: str               
    api_token: str              
    page_id: str                
    new_parent_id: str        

@router.put("/confluence/page/move")
def move_page(req: ConfluencePageMoveRequest):
    try:
        result = move_confluence_page(
            req.base_url,
            req.username,
            req.api_token,
            req.page_id,
            req.new_parent_id
        )
        return {
            "status": "success",
            "moved_page_id": result["id"],
            "link": result["_links"]["base"] + result["_links"]["webui"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
