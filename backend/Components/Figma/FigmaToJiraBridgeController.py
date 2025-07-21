from fastapi import APIRouter
from pydantic import BaseModel
from FigmaToJiraBridgeHelper import send_figma_to_jira

router = APIRouter()

class FigmaToJiraRequest(BaseModel):
    figma_token: str
    file_key: str
    jira_domain: str         
    jira_email: str          
    jira_token: str         
    issue_key: str           

@router.post("/figma/to-jira/post")
async def post_figma_to_jira(req: FigmaToJiraRequest):
    return send_figma_to_jira(
        figma_token=req.figma_token,
        file_key=req.file_key,
        jira_domain=req.jira_domain,
        jira_email=req.jira_email,
        jira_token=req.jira_token,
        issue_key=req.issue_key
    )