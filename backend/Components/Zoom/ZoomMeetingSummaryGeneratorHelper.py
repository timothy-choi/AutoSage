import requests
from datetime import datetime

def fetch_zoom_meeting_details(meeting_id, jwt_token):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch meeting: {response.text}")
    return response.json()

def fetch_zoom_meeting_participants(meeting_id, jwt_token):
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json().get("participants", [])

def generate_meeting_summary(meeting_data, participants):
    topic = meeting_data.get("topic", "Unnamed Meeting")
    start_time = meeting_data.get("start_time")
    duration = meeting_data.get("duration", 0)
    total_participants = len(participants)
    names = [p["name"] for p in participants]
    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00")) if start_time else None

    summary = f"📋 *Meeting Summary: {topic}*\n"
    if start_dt:
        summary += f"- 🕒 Held on: {start_dt.strftime('%B %d, %Y at %I:%M %p %Z')}\n"
    summary += f"- ⏱ Duration: {duration} minutes\n"
    summary += f"- 👥 Total Participants: {total_participants}\n"
    if total_participants > 0:
        summary += f"- 🧑‍🤝‍🧑 Participants: {', '.join(names[:5])}"
        if total_participants > 5:
            summary += f", and {total_participants - 5} more..."
        summary += "\n"

    summary += "\n✅ Summary generated automatically based on metadata."
    return summary