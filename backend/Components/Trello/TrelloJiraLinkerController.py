from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from TrelloToJiraLinkerHelper import extract_card_info, create_jira_issue, comment_on_trello_card

router = APIRouter()

class JiraConfig(BaseModel):
    jira_base_url: str
    jira_username: str
    jira_api_token: str
    jira_project_key: str
    trello_key: str
    trello_token: str

@router.post("/trello/webhook/jira", tags=["Trello to Jira"])
async def trello_to_jira_webhook(
    request: Request,
    config: JiraConfig
):
    try:
        payload = await request.json()
        card_data = extract_card_info(payload)
        if not card_data:
            return {"message": "No relevant Trello action to sync."}

        jira_auth = (config.jira_username, config.jira_api_token)
        jira_issue = create_jira_issue(
            jira_base_url=config.jira_base_url,
            auth=jira_auth,
            project_key=config.jira_project_key,
            card_name=card_data["name"],
            card_desc=card_data["desc"]
        )

        issue_key = jira_issue["key"]
        issue_url = f"{config.jira_base_url}/browse/{issue_key}"
        comment_on_trello_card(
            trello_key=config.trello_key,
            trello_token=config.trello_token,
            card_id=card_data["id"],
            jira_issue_url=issue_url
        )

        return {"status": "success", "jira_issue_key": issue_key, "jira_issue_url": issue_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))