import requests
from datetime import datetime, timedelta

def fetch_daily_meetings(user_id, jwt_token, date_str):
    date = datetime.fromisoformat(date_str)
    start_date = date.strftime('%Y-%m-%dT00:00:00Z')
    end_date = (date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {
        "type": "past",
        "from": start_date[:10],
        "to": end_date[:10],
        "page_size": 100
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch meetings: {response.text}")

    return response.json().get("meetings", [])

def format_meeting_summary(meeting):
    start_time = meeting.get("start_time", "")
    duration = meeting.get("duration", 0)
    topic = meeting.get("topic", "Untitled")
    join_url = meeting.get("join_url", "")

    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00")) if start_time else None
    time_str = start_dt.strftime("%I:%M %p") if start_dt else "Unknown Time"

    return f"- 🕒 *{topic}* at {time_str} for {duration} min\n  🔗 [Join Link]({join_url})"

def generate_daily_digest(meetings, date_str):
    if not meetings:
        return f"No Zoom meetings found on {date_str}."

    digest = f"📅 *Zoom Daily Digest for {date_str}*\n"
    for meeting in meetings:
        digest += format_meeting_summary(meeting) + "\n"
    return digest.strip()
