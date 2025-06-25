import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

def create_recurring_jira_issue(
    jira_base_url: str,
    email: str,
    api_token: str,
    project_key: str,
    summary_template: str,
    description_template: str = "",
    issue_type: str = "Task"
) -> dict:
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    today = datetime.utcnow().strftime("%Y-%m-%d")
    summary = summary_template.replace("{{date}}", today)
    description = description_template.replace("{{date}}", today)

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }

    url = f"{jira_base_url}/rest/api/2/issue"
    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        issue = response.json()
        return {
            "status": "created",
            "issue_key": issue["key"],
            "url": f"{jira_base_url}/browse/{issue['key']}"
        }
    else:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }