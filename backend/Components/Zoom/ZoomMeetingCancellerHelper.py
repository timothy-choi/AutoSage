import requests
from ZoomMeetingCancellerHelper import get_jwt_token

def cancel_zoom_meeting(api_key, api_secret, meeting_id):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"message": "Meeting successfully canceled"}
    else:
        return {"error": f"Failed to cancel meeting: {response.status_code} - {response.text}"}