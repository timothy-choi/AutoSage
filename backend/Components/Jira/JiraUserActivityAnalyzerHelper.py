import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

def analyze_jira_user_activity(
    jira_base_url: str,
    email: str,
    api_token: str,
    user_email: str,
    days: int = 7,
    max_results: int = 50
) -> dict:
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json"
    }

    since = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
    results = {}

    def run_jql(jql):
        url = f"{jira_base_url}/rest/api/2/search"
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "summary,status,updated"
        }
        res = requests.get(url, headers=headers, params=params, auth=auth)
        return res.json().get("issues", []) if res.status_code == 200 else []

    created_issues = run_jql(f'reporter = "{user_email}" AND created >= "{since}"')
    assigned_issues = run_jql(f'assignee = "{user_email}" AND updated >= "{since}"')

    comment_count = 0
    for issue in assigned_issues[:10]:
        key = issue["key"]
        comment_url = f"{jira_base_url}/rest/api/2/issue/{key}/comment"
        res = requests.get(comment_url, headers=headers, auth=auth)
        if res.status_code == 200:
            comments = res.json().get("comments", [])
            comment_count += sum(1 for c in comments if c.get("author", {}).get("emailAddress") == user_email)

    results["user_email"] = user_email
    results["window_days"] = days
    results["issues_created"] = len(created_issues)
    results["issues_assigned"] = len(assigned_issues)
    results["comments_made"] = comment_count
    results["recent_updates"] = [
        {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "updated": issue["fields"]["updated"]
        }
        for issue in assigned_issues
    ]

    return results