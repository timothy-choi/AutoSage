from fastapi import APIRouter
from pydantic import BaseModel
from FigmaToNotionBridgeHelper import (
    create_notion_page,
    format_figma_comment_entry,
    format_figma_update_entry
)

router = APIRouter()

class FigmaToNotionCommentRequest(BaseModel):
    notion_token: str
    database_id: str
    file_name: str
    commenter: str
    comment_text: str
    file_url: str

class FigmaToNotionActivityRequest(BaseModel):
    notion_token: str
    database_id: str
    file_name: str
    last_modified: str
    file_url: str

@router.post("/figma/to-notion/comment")
def post_figma_comment_to_notion(req: FigmaToNotionCommentRequest):
    content = format_figma_comment_entry(req.commenter, req.file_name, req.comment_text)
    return create_notion_page(
        notion_token=req.notion_token,
        database_id=req.database_id,
        title=f"Comment on {req.file_name}",
        content=content,
        figma_url=req.file_url
    )

@router.post("/figma/to-notion/activity")
def post_figma_activity_to_notion(req: FigmaToNotionActivityRequest):
    content = format_figma_update_entry(req.file_name, req.last_modified)
    return create_notion_page(
        notion_token=req.notion_token,
        database_id=req.database_id,
        title=f"Update: {req.file_name}",
        content=content,
        figma_url=req.file_url
    )