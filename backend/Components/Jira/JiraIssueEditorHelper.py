import requests
from requests.auth import HTTPBasicAuth

def edit_jira_issue(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    summary: str = None,
    description: str = None,
    issue_type: str = None,
    labels: list[str] = None
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields = {}
    if summary:
        fields["summary"] = summary
    if description:
        fields["description"] = description
    if issue_type:
        fields["issuetype"] = {"name": issue_type}
    if labels is not None:
        fields["labels"] = labels

    if not fields:
        return {"status": "error", "message": "No fields provided to update."}

    payload = {"fields": fields}
    response = requests.put(url, json=payload, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "updated",
            "issue_key": issue_key,
            "message": "Issue updated successfully."
        }
    else:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }