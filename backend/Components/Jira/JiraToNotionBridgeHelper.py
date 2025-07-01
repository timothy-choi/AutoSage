import requests

def fetch_jira_issues(jira_domain, project_key, jira_email, jira_token, max_results=5):
    url = f"https://{jira_domain}/rest/api/3/search"
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(jira_email, jira_token)}",
        "Accept": "application/json"
    }
    params = {
        "jql": f"project={project_key}",
        "maxResults": max_results
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Jira issues: {response.text}")

    return response.json().get("issues", [])

def create_notion_page_from_issue(issue, database_id, notion_token):
    issue_key = issue.get("key")
    fields = issue.get("fields", {})
    summary = fields.get("summary", "")
    status = fields.get("status", {}).get("name", "")
    priority = fields.get("priority", {}).get("name", "")
    assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
    url = f"https://{issue.get('self').split('/rest/')[0]}/browse/{issue_key}"

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"{issue_key}: {summary}"}}]
            },
            "Status": {
                "rich_text": [{"text": {"content": status}}]
            },
            "Priority": {
                "rich_text": [{"text": {"content": priority}}]
            },
            "Assignee": {
                "rich_text": [{"text": {"content": assignee}}]
            },
            "URL": {
                "url": url
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)
    return {
        "status": response.status_code,
        "notion_page_url": response.json().get("url") if response.status_code == 200 else None,
        "error": response.text if response.status_code != 200 else None,
        "jira_issue_key": issue_key
    }

def sync_jira_to_notion(jira_domain, project_key, jira_email, jira_token, notion_token, database_id, max_results=5):
    issues = fetch_jira_issues(jira_domain, project_key, jira_email, jira_token, max_results)
    results = []

    for issue in issues:
        result = create_notion_page_from_issue(issue, database_id, notion_token)
        results.append(result)

    return results