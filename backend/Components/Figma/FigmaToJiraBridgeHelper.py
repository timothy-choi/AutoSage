import requests

FIGMA_API_BASE = "https://api.figma.com/v1"

def fetch_figma_file_details(figma_token, file_key):
    headers = {"X-Figma-Token": figma_token}
    url = f"{FIGMA_API_BASE}/files/{file_key}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def extract_figma_summary(file_data):
    name = file_data.get("name", "Unknown")
    last_modified = file_data.get("lastModified", "N/A")
    thumbnail = file_data.get("thumbnailUrl", "N/A")

    return f"""🔗 **Figma File Summary**
- Name: {name}
- Last Modified: {last_modified}
- Thumbnail: {thumbnail}
"""

def post_comment_to_jira(jira_domain, jira_email, jira_token, issue_key, comment_body):
    url = f"https://{jira_domain}/rest/api/3/issue/{issue_key}/comment"
    auth = (jira_email, jira_token)
    headers = {"Content-Type": "application/json"}
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{
                    "text": comment_body,
                    "type": "text"
                }]
            }]
        }
    }
    resp = requests.post(url, auth=auth, json=payload, headers=headers)
    resp.raise_for_status()
    return {"status": "posted", "issue": issue_key}

def send_figma_to_jira(figma_token, file_key, jira_domain, jira_email, jira_token, issue_key):
    file_data = fetch_figma_file_details(figma_token, file_key)
    comment_body = extract_figma_summary(file_data)
    return post_comment_to_jira(jira_domain, jira_email, jira_token, issue_key, comment_body)