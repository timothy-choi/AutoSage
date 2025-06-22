from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookAutoTaggerHelper import (
    extract_entities_to_tag,
    inject_links_into_text
)

router = APIRouter()

class AutoTagInput(BaseModel):
    text: str

@router.post("/facebook/post/auto-tags")
def get_auto_tags(payload: AutoTagInput):
    try:
        entities = extract_entities_to_tag(payload.text)
        return {"detected_tags": entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/post/auto-link")
def link_entities(payload: AutoTagInput):
    try:
        entities = extract_entities_to_tag(payload.text)
        linked_text = inject_links_into_text(payload.text, entities)
        return {
            "original": payload.text,
            "linked": linked_text,
            "entities": entities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))