import requests
import uuid
from ZoomMeetingCreatorHelper import get_jwt_token 

def generate_update_payload(topic=None, start_time=None, duration=None, timezone=None, agenda=None, password=None):
    payload = {}

    if topic:
        payload["topic"] = topic
    if start_time:
        payload["start_time"] = start_time
    if duration:
        payload["duration"] = duration
    if timezone:
        payload["timezone"] = timezone
    if agenda:
        payload["agenda"] = agenda
    if password:
        payload["password"] = password
    if any(k in payload for k in ["topic", "start_time", "duration", "timezone", "agenda", "password"]):
        payload["settings"] = {
            "join_before_host": False,
            "waiting_room": True
        }

    return payload

def update_zoom_meeting(api_key, api_secret, meeting_id, topic=None, start_time=None, duration=None, timezone=None, agenda=None, password=None):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = generate_update_payload(topic, start_time, duration, timezone, agenda, password)
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"

    response = requests.patch(url, headers=headers, json=payload)
    return {
        "status_code": response.status_code,
        "message": "Meeting updated" if response.status_code == 204 else response.text
    }