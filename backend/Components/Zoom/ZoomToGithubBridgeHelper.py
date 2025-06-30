import requests
from datetime import datetime

def fetch_zoom_meetings(user_id, jwt_token, meeting_type="past"):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {
        "type": meeting_type,
        "page_size": 10
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Zoom meetings: {response.text}")
    
    return response.json().get("meetings", [])

def create_github_issue(repo_owner, repo_name, github_token, title, body):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "title": title,
        "body": body
    }

    response = requests.post(url, json=payload, headers=headers)
    return {
        "status": response.status_code,
        "url": response.json().get("html_url") if response.status_code == 201 else None,
        "error": response.text if response.status_code != 201 else None
    }

def sync_zoom_meetings_to_github(user_id, jwt_token, repo_owner, repo_name, github_token, meeting_type="past"):
    meetings = fetch_zoom_meetings(user_id, jwt_token, meeting_type)
    results = []

    for m in meetings:
        title = f"Zoom Meeting: {m.get('topic', 'Untitled')} ({m.get('id')})"
        start_time = m.get("start_time", "N/A")
        join_url = m.get("join_url", "N/A")
        duration = m.get("duration", "N/A")

        body = f"""
**Zoom Meeting Details**

- 🕒 Start Time: {start_time}
- ⏱ Duration: {duration} min
- 🔗 Join URL: {join_url}
- 🧾 Topic: {m.get('topic')}

_Auto-synced from Zoom by ZoomToGitHubBridge_
        """.strip()

        result = create_github_issue(repo_owner, repo_name, github_token, title, body)
        result["zoom_meeting_id"] = m.get("id")
        results.append(result)

    return results