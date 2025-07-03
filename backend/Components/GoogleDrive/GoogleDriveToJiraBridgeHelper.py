import requests

def send_drive_files_to_jira(
    files: list,
    jira_base_url: str,
    jira_email: str,
    jira_api_token: str,
    jira_project_key: str
) -> dict:
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(jira_email, jira_api_token)}",
        "Content-Type": "application/json"
    }

    created = []

    for file in files:
        name = file.get("name", "Unnamed file")
        mime = file.get("mimeType", "Unknown type")
        link = file.get("webViewLink", "")
        size = int(file.get("size", 0)) / (1024 * 1024)
        size_str = f"{size:.2f} MB" if size else "Unknown size"

        payload = {
            "fields": {
                "project": {"key": jira_project_key},
                "summary": f"Review: {name}",
                "description": (
                    f"*Type:* {mime}\n"
                    f"*Size:* {size_str}\n"
                    f"*Link:* {link}"
                ),
                "issuetype": {"name": "Task"}
            }
        }

        response = requests.post(
            f"{jira_base_url}/rest/api/3/issue",
            headers=headers,
            json=payload
        )

        if response.status_code not in (200, 201):
            raise Exception(f"Failed to create Jira issue: {response.text}")

        issue_key = response.json().get("key")
        created.append(issue_key)

    return {"status": "success", "created_issues": created}