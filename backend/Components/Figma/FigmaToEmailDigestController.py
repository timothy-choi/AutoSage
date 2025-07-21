from fastapi import APIRouter, Request
from pydantic import BaseModel
from FigmaToEmailDigestHelper import send_figma_email_digest

router = APIRouter()

class FigmaDigestRequest(BaseModel):
    figma_token: str
    team_id: str
    recipients: list[str]
    since_minutes: int = 1440

@router.post("/figma/to-email-digest/send")
async def send_figma_digest(req: FigmaDigestRequest):
    result = send_figma_email_digest(
        figma_token=req.figma_token,
        team_id=req.team_id,
        recipients=req.recipients,
        since_minutes=req.since_minutes
    )
    return result