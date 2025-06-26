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
    assignee: str = None
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type}
    }

    if assignee:
        fields["assignee"] = {"name": assignee}

    payload = {"fields": fields}

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 201:
        return {"key": response.json()["key"], "status": "created"}
    else:
        return {
            "status": "error",
            "error": response.text,
            "summary": summary
        }

def bulk_upload_issues(
    jira_base_url: str,
    email: str,
    api_token: str,
    project_key: str,
    issues: list
) -> list:
    results = []
    for issue in issues:
        result = create_jira_issue(
            jira_base_url=jira_base_url,
            email=email,
            api_token=api_token,
            project_key=project_key,
            summary=issue["summary"],
            description=issue.get("description", ""),
            issue_type=issue.get("issue_type", "Task"),
            assignee=issue.get("assignee")
        )
        results.append(result)
    return results