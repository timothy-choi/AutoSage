from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from NotionBlockRemoverHelper import delete_notion_block

router = APIRouter()

class NotionBlockDeleteRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    block_id: str = Field(..., description="Block ID to remove from the page")

@router.delete("/notion/delete-block")
def delete_notion_block_endpoint(request: NotionBlockDeleteRequest):
    try:
        result = delete_notion_block(
            notion_token=request.notion_token,
            block_id=request.block_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))