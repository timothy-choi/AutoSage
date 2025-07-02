import requests
from typing import List, Dict, Optional

NOTION_QUERY_API = "https://api.notion.com/v1/databases/{}/query"
NOTION_VERSION = "2022-06-28"

def fetch_notion_entries(notion_token: str, database_id: str, max_items: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    response = requests.post(NOTION_QUERY_API.format(database_id), headers=headers, json={"page_size": max_items})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch from Notion: {response.text}")
    return response.json().get("results", [])

def extract_jira_issue(entry: Dict) -> Optional[Dict]:
    props = entry.get("properties", {})
    title_prop = props.get("Name") or props.get("Title")
    title = title_prop.get("title", [{}])[0].get("plain_text") if title_prop else "Untitled"

    desc = props.get("Description", {}).get("rich_text", [])
    description = desc[0]["plain_text"] if desc else "Synced from Notion"
    tags = props.get("Tags", {}).get("multi_select", [])
    labels = [tag["name"] for tag in tags] if tags else []

    return {
        "summary": title,
        "description": description,
        "labels": labels
    }

def create_jira_issue(jira_email: str, jira_token: str, jira_base_url: str, project_key: str, issue_data: Dict) -> Dict:
    url = f"{jira_base_url}/rest/api/3/issue"
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(jira_email, jira_token)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "fields": {
            "project": { "key": project_key },
            "summary": issue_data["summary"],
            "description": issue_data["description"],
            "issuetype": { "name": "Task" },
            "labels": issue_data["labels"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return {
        "status": response.status_code,
        "title": issue_data["summary"],
        "jira_url": f"{jira_base_url}/browse/{response.json().get('key')}" if response.status_code == 201 else None,
        "error": None if response.status_code == 201 else response.text
    }

def sync_notion_to_jira(
    notion_token: str,
    database_id: str,
    jira_email: str,
    jira_token: str,
    jira_base_url: str,
    project_key: str,
    max_items: int = 10
) -> List[Dict]:
    notion_entries = fetch_notion_entries(notion_token, database_id, max_items)
    results = []
    for entry in notion_entries:
        issue_data = extract_jira_issue(entry)
        if issue_data:
            result = create_jira_issue(jira_email, jira_token, jira_base_url, project_key, issue_data)
            results.append(result)
    return results