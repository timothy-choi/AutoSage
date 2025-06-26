from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraToSlackBridgeHelper import bridge_jira_to_slack

router = APIRouter()

class JiraToSlackRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Jira issue key (e.g., BUG-101)")
    slack_webhook_url: str = Field(..., description="Slack incoming webhook URL")

@router.post("/jira/to-slack")
def jira_to_slack(request: JiraToSlackRequest):
    try:
        result = bridge_jira_to_slack(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            issue_key=request.issue_key,
            slack_webhook_url=request.slack_webhook_url
        )
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))