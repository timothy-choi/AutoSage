from fastapi import APIRouter, Query
from ConfluenceCommentAdderHelper import add_confluence_comment

router = APIRouter()

@router.post("/confluence/add-comment")
async def add_comment(
    page_id: str = Query(..., description="Confluence page ID to comment on"),
    comment: str = Query(..., description="Comment text in storage format")
):
    try:
        result = await add_confluence_comment(page_id, comment)
        return {"status": "success", "comment_id": result.get("id")}
    except Exception as e:
        return {"status": "error", "message": str(e)}