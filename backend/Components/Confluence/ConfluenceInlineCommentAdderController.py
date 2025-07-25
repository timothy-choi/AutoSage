from fastapi import APIRouter, Query
from ConfluenceInlineCommentAdderHelper import add_inline_comment

router = APIRouter()

@router.post("/confluence/add-inline-comment")
async def add_inline_comment_route(
    page_id: str = Query(..., description="Confluence page ID"),
    comment: str = Query(..., description="Comment text"),
    anchored_content_id: str = Query(..., description="ID of the content element to anchor the comment to")
):
    try:
        result = await add_inline_comment(page_id, comment, anchored_content_id)
        return {"status": "success", "comment_id": result.get("id")}
    except Exception as e:
        return {"status": "error", "message": str(e)}