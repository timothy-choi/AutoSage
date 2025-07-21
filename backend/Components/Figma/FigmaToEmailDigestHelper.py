import requests
from datetime import datetime, timedelta
from EmailController import send_user_email_helper  # Assume this is implemented

FIGMA_API_BASE = "https://api.figma.com/v1"

def get_recent_figma_activity(figma_token, team_id, since_minutes=1440):
    headers = {"X-Figma-Token": figma_token}
    cutoff_time = datetime.utcnow() - timedelta(minutes=since_minutes)

    projects_url = f"{FIGMA_API_BASE}/teams/{team_id}/projects"
    projects_resp = requests.get(projects_url, headers=headers)
    projects = projects_resp.json().get("projects", [])

    digest_data = []
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        
        files_url = f"{FIGMA_API_BASE}/projects/{project_id}/files"
        files_resp = requests.get(files_url, headers=headers)
        files = files_resp.json().get("files", [])

        for file in files:
            file_name = file['name']
            last_modified = datetime.strptime(file['last_modified'], "%Y-%m-%dT%H:%M:%SZ")
            if last_modified > cutoff_time:
                digest_data.append({
                    "project": project_name,
                    "file": file_name,
                    "last_modified": last_modified.isoformat()
                })

    return digest_data

def generate_email_body(digest_data):
    if not digest_data:
        return "No recent Figma updates in the last 24 hours."

    body = "📝 Recent Figma Activity Digest:\n\n"
    for item in digest_data:
        body += f"- Project: {item['project']}, File: {item['file']} (Updated: {item['last_modified']})\n"
    return body

def send_figma_email_digest(figma_token, team_id, recipients, since_minutes=1440):
    digest_data = get_recent_figma_activity(figma_token, team_id, since_minutes)
    email_body = generate_email_body(digest_data)
    send_user_email_helper("Daily Figma Activity Digest", recipients, email_body)
    return {"status": "sent", "count": len(digest_data)}