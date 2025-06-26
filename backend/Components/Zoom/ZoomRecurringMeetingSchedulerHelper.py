import requests
import uuid
from ZoomMeetingCreatorHelper import get_jwt_token

def generate_recurring_meeting_payload(topic, start_time, duration, recurrence, timezone="UTC", agenda="", password=None):
    return {
        "topic": topic,
        "type": 8,  
        "start_time": start_time,
        "duration": duration,
        "timezone": timezone,
        "agenda": agenda,
        "password": password or str(uuid.uuid4())[:10],
        "recurrence": recurrence,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "waiting_room": True,
            "approval_type": 0,  
        }
    }

def schedule_recurring_zoom_meeting(api_key, api_secret, user_id, topic, start_time, duration, recurrence, timezone="UTC", agenda="", password=None):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = generate_recurring_meeting_payload(topic, start_time, duration, recurrence, timezone, agenda, password)
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"

    response = requests.post(url, headers=headers, json=payload)
    return response.json()