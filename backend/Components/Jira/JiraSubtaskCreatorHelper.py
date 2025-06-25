import requests
from requests.auth import HTTPBasicAuth

def create_jira_subtask(
    jira_base_url: str,
    email: str,
    api_token: str,
    project_key: str,
    parent_issue_key: str,
    summary: str,
    description: str = "",
    subtask_type: str = "Sub-task",
    labels: list[str] = None
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields = {
        "project": {"key": project_key},
        "parent": {"key": parent_issue_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": subtask_type}
    }

    if labels:
        fields["labels"] = labels

    payload = {"fields": fields}

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        issue = response.json()
        return {
            "status": "created",
            "subtask_key": issue["key"],
            "subtask_url": f"{jira_base_url}/browse/{issue['key']}"
        }
    else:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }