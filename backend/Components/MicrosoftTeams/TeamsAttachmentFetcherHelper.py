import requests

GRAPH_API = "https://graph.microsoft.com/v1.0"

def list_attachments_in_channel_message(
    access_token: str,
    team_id: str,
    channel_id: str,
    message_id: str
) -> list:
    url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/messages/{message_id}/attachments"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])


def download_attachment_by_url(
    access_token: str,
    attachment_url: str
) -> bytes:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(attachment_url, headers=headers)
    response.raise_for_status()
    return response.content