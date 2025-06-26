import requests
from ZoomMeetingCreatorHelper import get_jwt_token, generate_meeting_payload

def fetch_meeting_details(api_key, api_secret, meeting_id):
    token = get_jwt_token(api_key, api_secret)
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else {"error": response.text}

def clone_zoom_meeting(api_key, api_secret, user_id, original_meeting_id, new_start_time=None):
    original = fetch_meeting_details(api_key, api_secret, original_meeting_id)

    if "error" in original:
        return original

    topic = f"{original.get('topic', 'Cloned Meeting')} (Clone)"
    duration = original.get("duration", 30)
    timezone = original.get("timezone", "UTC")
    agenda = original.get("agenda", "")
    password = original.get("password", None)
    new_time = new_start_time or original.get("start_time")

    payload = generate_meeting_payload(
        topic=topic,
        start_time=new_time,
        duration=duration,
        timezone=timezone,
        agenda=agenda,
        password=password
    )

    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    response = requests.post(url, headers=headers, json=payload)

    return response.json() if response.ok else {"error": response.text}