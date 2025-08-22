import requests

def extract_card_info(payload: dict):
    action = payload.get("action", {})
    type_ = action.get("type", "")
    if type_ not in {"createCard", "updateCard"}:
        return None

    card = action.get("data", {}).get("card", {})
    return {
        "name": card.get("name", ""),
        "desc": card.get("desc", ""),
        "id": card.get("id", "")
    }

def create_jira_issue(jira_base_url, auth, project_key, card_name, card_desc):
    url = f"{jira_base_url}/rest/api/3/issue"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": card_name,
            "description": card_desc,
            "issuetype": {
                "name": "Task"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload, auth=auth)
    response.raise_for_status()
    return response.json()

def comment_on_trello_card(trello_key, trello_token, card_id, jira_issue_url):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {
        "key": trello_key,
        "token": trello_token,
        "text": f"Linked Jira issue: {jira_issue_url}"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()