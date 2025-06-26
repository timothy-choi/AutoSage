import requests
from requests.auth import HTTPBasicAuth

def fetch_jira_issue(jira_base_url, email, api_token, issue_key):
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Jira issue: {response.text}")

    data = response.json()
    summary = data["fields"]["summary"]
    description = data["fields"].get("description", "(No description provided)")
    status = data["fields"]["status"]["name"]
    assignee = data["fields"].get("assignee", {}).get("displayName", "Unassigned")
    issue_url = f"{jira_base_url}/browse/{issue_key}"

    return {
        "key": issue_key,
        "summary": summary,
        "description": description,
        "status": status,
        "assignee": assignee,
        "url": issue_url
    }

def post_to_slack(slack_webhook_url: str, message: str) -> dict:
    payload = {
        "text": message
    }
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code == 200:
        return {"status": "sent"}
    else:
        return {"status": "error", "message": response.text, "code": response.status_code}

def bridge_jira_to_slack(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    slack_webhook_url: str
) -> dict:
    issue = fetch_jira_issue(jira_base_url, email, api_token, issue_key)

    message = (
        f"*Jira Issue* <{issue['url']}|{issue['key']}>: *{issue['summary']}*\n"
        f"> *Status:* {issue['status']} | *Assignee:* {issue['assignee']}\n"
        f"> *Description:* {issue['description'][:300]}{'...' if len(issue['description']) > 300 else ''}"
    )

    return post_to_slack(slack_webhook_url, message)