import requests
from requests.auth import HTTPBasicAuth

def auto_close_jira_issue(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    done_keywords: list[str] = ["done", "closed", "resolved"]
) -> dict:
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    transitions_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/transitions"
    response = requests.get(transitions_url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Could not fetch transitions: {response.text}"
        }

    transitions = response.json().get("transitions", [])
    match = next(
        (t for t in transitions if t["to"]["name"].strip().lower() in done_keywords),
        None
    )

    if not match:
        return {
            "status": "error",
            "message": f"No valid transition found to a terminal state ({done_keywords})"
        }

    transition_id = match["id"]
    close_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/transitions"
    payload = {"transition": {"id": transition_id}}

    result = requests.post(close_url, headers=headers, auth=auth, json=payload)

    if result.status_code == 204:
        return {
            "status": "success",
            "issue_key": issue_key,
            "new_status": match["to"]["name"]
        }

    return {
        "status": "error",
        "message": f"Transition failed: {result.text}"
    }