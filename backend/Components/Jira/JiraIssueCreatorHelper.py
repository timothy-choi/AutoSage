import requests
from requests.auth import HTTPBasicAuth

def create_jira_issue(
    jira_base_url: str,
    email: str,
    api_token: str,
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Task",
    labels: list[str] = None
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue"
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    issue_data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }

    if labels:
        issue_data["fields"]["labels"] = labels

    response = requests.post(url, json=issue_data, headers=headers, auth=auth)

    if response.status_code == 201:
        issue = response.json()
        return {
            "status": "created",
            "issue_key": issue["key"],
            "issue_url": f"{jira_base_url}/browse/{issue['key']}"
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "code": response.status_code
        }