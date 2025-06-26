import requests
from ZoomMeetingCreatorHelper import get_jwt_token

def get_meeting_start_and_join_info(api_key, api_secret, meeting_id):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "topic": data.get("topic"),
            "start_time": data.get("start_time"),
            "status": data.get("status"),
            "start_url": data.get("start_url"),
            "join_url": data.get("join_url")
        }
    else:
        return {"error": f"Failed to retrieve meeting info: {response.text}"}