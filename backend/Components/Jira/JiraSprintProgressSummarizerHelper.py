import requests
from requests.auth import HTTPBasicAuth
from collections import Counter

def summarize_jira_sprint_progress(
    jira_base_url: str,
    email: str,
    api_token: str,
    board_id: int,
    sprint_id: int
) -> dict:
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json"
    }

    url = f"{jira_base_url}/rest/agile/1.0/board/{board_id}/sprint/{sprint_id}/issue"
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to fetch sprint issues: {response.text}"
        }

    issues = response.json().get("issues", [])
    status_counter = Counter()
    assignee_counter = Counter()
    detailed_issues = []

    for issue in issues:
        status = issue["fields"]["status"]["name"]
        assignee = issue["fields"].get("assignee", {}).get("displayName", "Unassigned")
        status_counter[status] += 1
        assignee_counter[assignee] += 1
        detailed_issues.append({
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": status,
            "assignee": assignee
        })

    return {
        "status": "success",
        "total_issues": len(issues),
        "status_breakdown": dict(status_counter),
        "assignee_breakdown": dict(assignee_counter),
        "issues": detailed_issues
    }