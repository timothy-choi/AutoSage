from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from TrelloToGoogleSheetExporterHelper import get_trello_board_data, export_to_google_sheets

router = APIRouter()

class ExportRequest(BaseModel):
    trello_api_key: str
    trello_token: str
    board_id: str
    google_sheet_id: str
    worksheet_name: str
    credentials_json_path: str  


@router.post("/trello/export-to-google-sheets")
def export_trello_to_google_sheets(req: ExportRequest):
    try:
        cards = get_trello_board_data(req.trello_api_key, req.trello_token, req.board_id)
        export_to_google_sheets(req.google_sheet_id, req.worksheet_name, cards, req.credentials_json_path)
        return {"status": "success", "message": f"{len(cards)} cards exported successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))