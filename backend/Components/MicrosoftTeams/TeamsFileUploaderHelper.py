import requests

GRAPH_API = "https://graph.microsoft.com/v1.0"

def upload_file_to_channel(
    access_token: str,
    team_id: str,
    channel_id: str,
    file_name: str,
    file_bytes: bytes
) -> dict:
    site_url = f"{GRAPH_API}/teams/{team_id}/channels/{channel_id}/filesFolder"
    headers = {"Authorization": f"Bearer {access_token}"}
    site_response = requests.get(site_url, headers=headers)
    site_response.raise_for_status()
    folder = site_response.json()
    folder_id = folder["id"]

    upload_url = f"{GRAPH_API}/drives/{folder['parentReference']['driveId']}/items/{folder_id}:/{file_name}:/content"
    upload_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    upload_response = requests.put(upload_url, headers=upload_headers, data=file_bytes)
    upload_response.raise_for_status()

    return upload_response.json()