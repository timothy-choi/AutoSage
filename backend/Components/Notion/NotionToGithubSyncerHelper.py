import requests
from typing import List, Dict, Optional

NOTION_API_URL = "https://api.notion.com/v1/databases/{}/query"
NOTION_VERSION = "2022-06-28"

def fetch_notion_entries(notion_token: str, database_id: str, max_items: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    response = requests.post(NOTION_API_URL.format(database_id), headers=headers, json={"page_size": max_items})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch from Notion: {response.text}")
    return response.json().get("results", [])

def extract_issue_data(entry: Dict) -> Optional[Dict]:
    props = entry.get("properties", {})
    title_prop = props.get("Name") or props.get("Title")
    title = title_prop.get("title", [{}])[0].get("plain_text") if title_prop else "Untitled"

    tags = props.get("Tags", {}).get("multi_select", [])
    labels = [t["name"] for t in tags] if tags else []

    status = props.get("Status", {}).get("select", {}).get("name", "")
    body = f"Synced from Notion\n\nStatus: {status}\n\nPage: {entry.get('url', '')}"

    return {
        "title": title,
        "body": body,
        "labels": labels
    }

def create_github_issue(github_token: str, repo_full_name: str, issue_data: Dict) -> Dict:
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(url, headers=headers, json=issue_data)
    return {
        "status": response.status_code,
        "title": issue_data.get("title"),
        "issue_url": response.json().get("html_url") if response.status_code == 201 else None,
        "error": None if response.status_code == 201 else response.text
    }

def sync_notion_to_github(notion_token: str, database_id: str, github_token: str, repo: str, max_items: int = 10) -> List[Dict]:
    entries = fetch_notion_entries(notion_token, database_id, max_items)
    results = []
    for entry in entries:
        issue_data = extract_issue_data(entry)
        if issue_data:
            result = create_github_issue(github_token, repo, issue_data)
            results.append(result)
    return results