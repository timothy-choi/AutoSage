import requests
from requests.auth import HTTPBasicAuth
from collections import Counter

def fetch_jira_issues_for_status_distribution(
    jira_base_url: str,
    email: str,
    api_token: str,
    jql: str,
    max_results: int = 500
) -> list:
    url = f"{jira_base_url}/rest/api/2/search"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}
    
    params = {
        "jql": jql,
        "maxResults": max_results,
        "fields": "status"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch issues: {response.text}")

    return response.json()["issues"]

def compute_status_distribution(issues: list) -> dict:
    status_counts = Counter()
    for issue in issues:
        status = issue["fields"]["status"]["name"]
        status_counts[status] += 1
    return dict(status_counts)

def get_jira_status_distribution(
    jira_base_url: str,
    email: str,
    api_token: str,
    project_key: str = None,
    custom_jql: str = None
) -> dict:
    jql = custom_jql or f"project = {project_key}"
    issues = fetch_jira_issues_for_status_distribution(jira_base_url, email, api_token, jql)
    return compute_status_distribution(issues)