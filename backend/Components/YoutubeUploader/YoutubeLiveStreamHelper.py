import requests

BASE_URL = "https://www.googleapis.com/youtube/v3"

def create_live_stream(access_token: str, title: str, description: str, privacy_status: str = "public"):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    stream_url = f"{BASE_URL}/liveStreams?part=snippet,cdn"
    stream_payload = {
        "snippet": {
            "title": title,
            "description": description
        },
        "cdn": {
            "frameRate": "30fps",
            "resolution": "720p",
            "ingestionType": "rtmp"
        }
    }
    stream_resp = requests.post(stream_url, headers=headers, json=stream_payload)
    if stream_resp.status_code not in (200, 201):
        raise Exception(f"Failed to create live stream: {stream_resp.text}")
    stream_data = stream_resp.json()

    broadcast_url = f"{BASE_URL}/liveBroadcasts?part=snippet,status,contentDetails"
    broadcast_payload = {
        "snippet": {
            "title": title,
            "description": description,
            "scheduledStartTime": None  
        },
        "status": {
            "privacyStatus": privacy_status
        },
        "contentDetails": {
            "boundStreamId": stream_data["id"]
        }
    }
    broadcast_resp = requests.post(broadcast_url, headers=headers, json=broadcast_payload)
    if broadcast_resp.status_code not in (200, 201):
        raise Exception(f"Failed to create live broadcast: {broadcast_resp.text}")

    return {
        "stream": stream_data,
        "broadcast": broadcast_resp.json()
    }


def list_scheduled_streams(access_token: str, max_results: int = 10):
    url = f"{BASE_URL}/liveBroadcasts?part=snippet,status&broadcastStatus=upcoming&maxResults={max_results}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to list scheduled streams: {response.text}")
    return response.json()


def end_live_broadcast(access_token: str, broadcast_id: str):  
    url = f"{BASE_URL}/liveBroadcasts?part=status"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "id": broadcast_id,
        "status": {
            "lifeCycleStatus": "complete"
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to end live broadcast: {response.text}")
    return response.json()