from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from NotionBlockEditorHelper import edit_notion_block

router = APIRouter()

class NotionBlockEditRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    block_id: str = Field(..., description="The ID of the block to edit")
    block_type: Literal["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]
    new_text: str = Field(..., description="The new text content for the block")

@router.patch("/notion/edit-block")
def edit_notion_block_endpoint(request: NotionBlockEditRequest):
    try:
        result = edit_notion_block(
            notion_token=request.notion_token,
            block_id=request.block_id,
            block_type=request.block_type,
            new_text=request.new_text
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))