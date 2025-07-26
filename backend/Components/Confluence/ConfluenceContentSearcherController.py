from fastapi import APIRouter, Query
from ConfluenceContentSearcherHelper import search_confluence_content

router = APIRouter()

@router.get("/confluence/search-content")
async def search_confluence(
    title: str = Query(None, description="Search by title"),
    label: str = Query(None, description="Search by label"),
    content_type: str = Query("page", description="Type of content: page, blogpost, etc."),
    cql: str = Query(None, description="Optional full Confluence Query Language (CQL)"),
    limit: int = Query(10, description="Max number of results")
):
    try:
        results = await search_confluence_content(
            title=title,
            label=label,
            content_type=content_type,
            cql=cql,
            limit=limit
        )
        return {"status": "success", "results": results.get("results", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}