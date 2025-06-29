import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

def fetch_meeting_details(meeting_id, jwt_token):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching meeting: {response.text}")
    return response.json()

def fetch_participants(meeting_id, jwt_token):
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json().get("participants", [])

def calculate_engagement_score(participants, meeting_duration):
    if not participants or meeting_duration <= 0:
        return {"score": 0, "reason": "No participants or invalid duration."}

    total_minutes = 0
    for p in participants:
        duration = p.get("duration", 0)
        total_minutes += duration

    avg_duration = total_minutes / len(participants)
    raw_score = (len(participants) * avg_duration) / meeting_duration
    score = round(min(100, raw_score * 10), 2) 

    return {
        "score": score,
        "participants_count": len(participants),
        "average_participant_duration": round(avg_duration, 2),
        "total_meeting_duration": meeting_duration
    }

def generate_zoom_engagement_report(meeting_id, jwt_token):
    meeting = fetch_meeting_details(meeting_id, jwt_token)
    participants = fetch_participants(meeting_id, jwt_token)

    duration = meeting.get("duration", 0)
    result = calculate_engagement_score(participants, duration)
    result["topic"] = meeting.get("topic", "Untitled")
    result["meeting_id"] = meeting_id
    return result