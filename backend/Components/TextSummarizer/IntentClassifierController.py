from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from IntentClassifierHelper import classify_intent, rank_intents, is_intent_match

router = APIRouter()

class IntentRequest(BaseModel):
    text: str
    candidate_labels: List[str] = []

class MatchRequest(BaseModel):
    text: str
    expected_intent: str

@router.post("/intent/classify")
def classify(data: IntentRequest):
    try:
        result = classify_intent(data.text, data.candidate_labels or None)
        return {"predicted_intent": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intent/rank")
def rank(data: IntentRequest):
    try:
        results = rank_intents(data.text, data.candidate_labels or None)
        return {"ranked_intents": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intent/match")
def match(data: MatchRequest):
    try:
        matched = is_intent_match(data.text, data.expected_intent)
        return {"is_match": matched}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))