from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from TrelloToNotionSyncerHelper import extract_card_data, create_notion_page

router = APIRouter()

class NotionSyncConfig(BaseModel):
    notion_token: str = Field(..., description="Integration token for Notion")
    database_id: str = Field(..., description="Target Notion database ID")

@router.post("/trello/webhook/notion", tags=["Trello to Notion"])
async def trello_to_notion_webhook(
    request: Request,
    config: NotionSyncConfig
):
    try:
        payload = await request.json()
        card_data = extract_card_data(payload)
        if not card_data:
            return {"message": "No sync needed for this event."}

        result = create_notion_page(
            token=config.notion_token,
            database_id=config.database_id,
            title=card_data["title"],
            description=card_data["description"]
        )
        return {"status": "success", "notion_page_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))