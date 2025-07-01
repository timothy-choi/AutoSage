from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from NotionBlockAddrHelper import add_blocks_to_notion_page, build_block

router = APIRouter()

class BlockInput(BaseModel):
    type: Literal["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]
    content: str

class NotionBlockAddRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    page_id: str = Field(..., description="Notion page ID")
    blocks: List[BlockInput] = Field(..., description="List of blocks to add")

@router.post("/notion/add-blocks")
def add_blocks_endpoint(request: NotionBlockAddRequest):
    try:
        block_payloads = [build_block(b.type, b.content) for b in request.blocks]
        result = add_blocks_to_notion_page(
            notion_token=request.notion_token,
            page_id=request.page_id,
            blocks=block_payloads
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))