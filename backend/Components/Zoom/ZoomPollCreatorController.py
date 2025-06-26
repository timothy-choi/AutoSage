from fastapi import APIRouter, Body, Query
from typing import List, Dict
from ZoomPollCreatorHelper import create_zoom_poll
import os

router = APIRouter()

ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")

@router.post("/zoom/meeting/poll/create")
def create_poll(
    meeting_id: str = Query(..., description="Zoom meeting ID"),
    title: str = Query(..., description="Poll title"),
    questions: List[Dict] = Body(..., description="""
        List of question objects, each with:
        - name: question text
        - type: 'single' or 'multiple'
        - answers: list of answer choices
    """)
):
    if not ZOOM_API_KEY or not ZOOM_API_SECRET:
        return {"error": "Missing Zoom API credentials"}

    try:
        result = create_zoom_poll(ZOOM_API_KEY, ZOOM_API_SECRET, meeting_id, title, questions)
        return result
    except Exception as e:
        return {"error": str(e)}