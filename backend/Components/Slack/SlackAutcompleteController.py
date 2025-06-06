from fastapi import APIRouter, Query
from typing import Dict, List
from SlackAutocompleteHelper import autocomplete_command_fuzzy

router = APIRouter()

@router.get("/slack/autocomplete/fuzzy")
def get_fuzzy_command_suggestions(
    input: str = Query(..., description="Partial command text"),
    limit: int = Query(5, description="Max number of suggestions")
) -> Dict[str, List[str]]:
    return autocomplete_command_fuzzy(input, limit)