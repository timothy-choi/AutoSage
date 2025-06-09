import requests

GRAPH_API = "https://graph.microsoft.com/v1.0"

def reply_to_thread_message(
    access_token: str,
    team_id: str,
    channel_id: str,
    parent_message_id: str,
    reply_text: str
) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages/{parent_message_id}/replies"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "body": {
            "content": reply_text
        }
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()

def reply_with_markdown(access_token, team_id, channel_id, parent_message_id, markdown: str) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages/{parent_message_id}/replies"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    body = {"body": {"contentType": "html", "content": markdown}}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()

def reply_with_mention(access_token, team_id, channel_id, parent_message_id, user_id, display_name, message: str) -> dict:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages/{parent_message_id}/replies"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    body = {
        "body": {
            "contentType": "html",
            "content": f'<at id="0">{display_name}</at> {message}'
        },
        "mentions": [
            {
                "id": 0,
                "mentionText": display_name,
                "mentioned": {
                    "user": {
                        "id": user_id,
                        "displayName": display_name
                    }
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()