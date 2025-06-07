from fastapi import APIRouter, Query
from DiscordCommandAutocompleterHelper import autocomplete_command

router = APIRouter()

@router.get("/discord/autocomplete")
def get_command_suggestions(
    input_text: str = Query(..., description="Partial input to autocomplete"),
    limit: int = Query(5, description="Max number of suggestions")
):
    try:
        results = autocomplete_command(input_text, limit)
        return {"suggestions": results}
    except Exception as e:
        return {"error": str(e)}