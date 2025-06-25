import requests
from requests.auth import HTTPBasicAuth

def delete_jira_issue(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Issue {issue_key} deleted successfully."
        }
    elif response.status_code == 404:
        return {
            "status": "error",
            "message": f"Issue {issue_key} not found."
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to delete issue: {response.text}"
        }