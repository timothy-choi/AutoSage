import requests
from datetime import datetime

def fetch_figma_activity(access_token: str, team_id: str) -> dict:
    headers = {
        "X-Figma-Token": access_token
    }

    team_projects_url = f"https://api.figma.com/v1/teams/{team_id}/projects"
    project_response = requests.get(team_projects_url, headers=headers)

    if project_response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch team projects",
            "details": project_response.json()
        }

    projects = project_response.json().get("projects", [])
    activity_log = []

    for project in projects:
        project_id = project.get("id")
        project_name = project.get("name")
        files_url = f"https://api.figma.com/v1/projects/{project_id}/files"
        files_response = requests.get(files_url, headers=headers)

        if files_response.status_code != 200:
            continue

        files = files_response.json().get("files", [])
        for file in files:
            activity_log.append({
                "file_name": file.get("name"),
                "last_modified": file.get("last_modified"),
                "project_name": project_name,
                "project_id": project_id,
                "file_key": file.get("key"),
                "thumbnail_url": file.get("thumbnail_url"),
            })

    activity_log.sort(key=lambda x: x["last_modified"], reverse=True)
    return {
        "status": "success",
        "message": f"Fetched recent activity for team {team_id}",
        "activity_log": activity_log
    }