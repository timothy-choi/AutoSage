from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraSmartCommentResponderHelper import generate_smart_jira_reply, post_comment_to_jira

router = APIRouter()

class JiraSmartReplyRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Your Atlassian email")
    api_token: str = Field(..., description="Your Jira API token")
    issue_key: str = Field(..., description="Jira issue key to comment on")
    issue_summary: str = Field(..., description="Issue title/summary")
    issue_description: str = Field(..., description="Issue description text")
    comment_text: str = Field(..., description="User comment to respond to")
    openai_api_key: str = Field(..., description="Your OpenAI API key")
    post_back: bool = Field(default=True, description="If true, post response to Jira")

@router.post("/jira/smart-comment-response")
def smart_comment_response(request: JiraSmartReplyRequest):
    try:
        smart_reply = generate_smart_jira_reply(
            issue_summary=request.issue_summary,
            issue_description=request.issue_description,
            comment_text=request.comment_text,
            openai_api_key=request.openai_api_key
        )

        if not request.post_back:
            return {"status": "generated", "reply": smart_reply}

        result = post_comment_to_jira(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            issue_key=request.issue_key,
            comment=smart_reply
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))