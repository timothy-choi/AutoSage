import requests
from requests.auth import HTTPBasicAuth

def fetch_jira_issue(jira_base_url, email, api_token, issue_key):
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        data = response.json()
        summary = data["fields"]["summary"]
        description = data["fields"].get("description", "")
        jira_url = f"{jira_base_url}/browse/{issue_key}"
        return {
            "summary": summary,
            "description": description,
            "url": jira_url
        }
    else:
        raise Exception(f"Failed to fetch Jira issue: {response.text}")

def create_github_issue(owner, repo, github_token, title, body):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "title": title,
        "body": body
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return {
            "status": "created",
            "issue_number": response.json()["number"],
            "github_url": response.json()["html_url"]
        }
    else:
        raise Exception(f"Failed to create GitHub issue: {response.text}")

def sync_jira_to_github(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    github_owner: str,
    github_repo: str,
    github_token: str
) -> dict:
    issue = fetch_jira_issue(jira_base_url, email, api_token, issue_key)

    title = f"[JIRA {issue_key}] {issue['summary']}"
    body = f"**Jira Issue:** [{issue_key}]({issue['url']})\n\n{issue['description']}"

    result = create_github_issue(
        owner=github_owner,
        repo=github_repo,
        github_token=github_token,
        title=title,
        body=body
    )

    return result