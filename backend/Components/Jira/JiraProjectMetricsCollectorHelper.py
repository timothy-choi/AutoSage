import requests
from requests.auth import HTTPBasicAuth
from collections import Counter

def fetch_jira_project_issues(jira_base_url, email, api_token, project_key, max_results=500):
    url = f"{jira_base_url}/rest/api/2/search"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    params = {
        "jql": f"project = {project_key}",
        "maxResults": max_results,
        "fields": "status,issuetype"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch project issues: {response.text}")

    return response.json()["issues"]

def calculate_project_metrics(issues):
    status_counts = Counter()
    type_counts = Counter()

    for issue in issues:
        status = issue["fields"]["status"]["name"]
        issue_type = issue["fields"]["issuetype"]["name"]
        status_counts[status] += 1
        type_counts[issue_type] += 1

    total = len(issues)
    open_issues = sum(v for k, v in status_counts.items() if k.lower() not in ["done", "closed", "resolved"])
    closed_issues = total - open_issues

    return {
        "total_issues": total,
        "open_issues": open_issues,
        "closed_issues": closed_issues,
        "issues_by_status": dict(status_counts),
        "issues_by_type": dict(type_counts)
    }

def collect_jira_project_metrics(jira_base_url, email, api_token, project_key):
    issues = fetch_jira_project_issues(jira_base_url, email, api_token, project_key)
    return calculate_project_metrics(issues)