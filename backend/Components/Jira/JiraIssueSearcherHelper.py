import requests
from requests.auth import HTTPBasicAuth

def search_jira_issues(
    jira_base_url: str,
    email: str,
    api_token: str,
    jql: str,
    max_results: int = 10
) -> dict:
    url = f"{jira_base_url}/rest/api/2/search"
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "jql": jql,
        "maxResults": max_results
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        issues = [
            {
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
                "assignee": issue["fields"].get("assignee", {}).get("displayName"),
                "created": issue["fields"]["created"]
            }
            for issue in data.get("issues", [])
        ]
        return {
            "status": "success",
            "total": data.get("total", 0),
            "issues": issues
        }
    else:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }