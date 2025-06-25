import requests
from requests.auth import HTTPBasicAuth

def update_jira_status(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    target_status: str
) -> dict:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(email, api_token)

    transitions_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/transitions"
    transitions_response = requests.get(transitions_url, headers=headers, auth=auth)

    if transitions_response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to fetch transitions. {transitions_response.text}"
        }

    transitions = transitions_response.json().get("transitions", [])
    matching = next((t for t in transitions if t["to"]["name"].lower() == target_status.lower()), None)

    if not matching:
        return {
            "status": "error",
            "message": f"No valid transition found for target status '{target_status}'."
        }

    transition_id = matching["id"]
    update_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/transitions"
    payload = {"transition": {"id": transition_id}}

    update_response = requests.post(update_url, json=payload, headers=headers, auth=auth)

    if update_response.status_code == 204:
        return {
            "status": "success",
            "issue_key": issue_key,
            "new_status": target_status
        }
    else:
        return {
            "status": "error",
            "message": f"Transition failed. {update_response.text}"
        }