import requests
from requests.auth import HTTPBasicAuth

def filter_issues_by_label(
    jira_base_url: str,
    email: str,
    api_token: str,
    labels: list,
    max_results: int = 10
) -> list:
    jql_labels = " OR ".join([f'labels = "{label}"' for label in labels])
    jql = f"({jql_labels}) ORDER BY created DESC"

    url = f"{jira_base_url}/rest/api/2/search"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    params = {
        "jql": jql,
        "maxResults": max_results,
        "fields": "summary,status,assignee,labels"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch issues: {response.text}")

    issues = []
    for issue in response.json()["issues"]:
        fields = issue["fields"]
        issues.append({
            "key": issue["key"],
            "summary": fields["summary"],
            "status": fields["status"]["name"],
            "assignee": fields.get("assignee", {}).get("displayName", "Unassigned"),
            "labels": fields.get("labels", [])
        })

    return issues