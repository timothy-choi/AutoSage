import requests
from requests.auth import HTTPBasicAuth

def add_jira_comment(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    comment_body: str
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/comment"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "body": comment_body
    }

    response = requests.post(url, headers=headers, json=payload, auth=auth)

    if response.status_code == 201:
        comment = response.json()
        return {
            "status": "success",
            "comment_id": comment["id"],
            "comment": comment["body"],
            "issue_key": issue_key
        }

    return {
        "status": "error",
        "code": response.status_code,
        "message": response.text
    }