from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsFormToJiraBridgerHelper import (
    create_jira_ticket,
    add_comment_to_ticket,
    update_ticket_status
)

router = APIRouter()

class JiraTicketRequest(BaseModel):
    jira_url: str
    auth_token: str
    project_key: str
    summary: str
    description: str
    issue_type: str = "Task"

class JiraCommentRequest(BaseModel):
    jira_url: str
    auth_token: str
    issue_key: str
    comment: str

class JiraStatusUpdateRequest(BaseModel):
    jira_url: str
    auth_token: str
    issue_key: str
    transition_id: str

@router.post("/teams/form-to-jira")
async def form_to_jira(req: JiraTicketRequest):
    result = await create_jira_ticket(
        req.jira_url,
        req.auth_token,
        req.project_key,
        req.summary,
        req.description,
        req.issue_type
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/jira-add-comment")
async def jira_add_comment(req: JiraCommentRequest):
    result = await add_comment_to_ticket(req.jira_url, req.auth_token, req.issue_key, req.comment)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/jira-update-status")
async def jira_update_status(req: JiraStatusUpdateRequest):
    result = await update_ticket_status(req.jira_url, req.auth_token, req.issue_key, req.transition_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result