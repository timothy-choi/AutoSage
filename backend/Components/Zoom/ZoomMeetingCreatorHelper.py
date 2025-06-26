import requests
import datetime
import uuid

def get_jwt_token(api_key, api_secret):
    import jwt
    import time
    payload = {
        'iss': api_key,
        'exp': int(time.time()) + 3600
    }
    return jwt.encode(payload, api_secret, algorithm='HS256')

def generate_meeting_payload(topic, start_time, duration, timezone="UTC", agenda="", password=None):
    return {
        "topic": topic,
        "type": 2, 
        "start_time": start_time,  
        "duration": duration,  
        "timezone": timezone,
        "agenda": agenda,
        "password": password or str(uuid.uuid4())[:10],
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "waiting_room": True,
        }
    }

def create_zoom_meeting(api_key, api_secret, user_id, topic, start_time, duration, timezone="UTC", agenda="", password=None):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = generate_meeting_payload(topic, start_time, duration, timezone, agenda, password)
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"

    response = requests.post(url, headers=headers, json=payload)
    return response.json()